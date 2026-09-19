"""Limited offline ComfyUI API-prompt inspection. Never runs or installs nodes."""
from __future__ import annotations
import math
from .common import ACOError

def comfy_preflight(prompt: dict, object_info: dict) -> dict:
    if not isinstance(prompt,dict) or not prompt:
        raise ACOError('Provide a nonempty API prompt object, not a UI workflow export.')
    if isinstance(prompt.get('nodes'),list):
        raise ACOError('This is UI workflow JSON. Export API prompt JSON before preflight.')
    if not isinstance(object_info,dict) or not object_info:
        raise ACOError('Provide an object_info snapshot from the target authorized environment.')
    graph={str(k):v for k,v in prompt.items()}
    errors=[];warnings=[];links={k:[] for k in graph}
    for node_id,node in graph.items():
        if not isinstance(node,dict) or not isinstance(node.get('inputs'),dict) or not isinstance(node.get('class_type'),str):
            errors.append(f'{node_id}: expected class_type and inputs object');continue
        klass=node['class_type'];schema=object_info.get(klass)
        if not isinstance(schema,dict):
            errors.append(f'{node_id}: node type not registered in supplied snapshot: {klass}');continue
        ins=schema.get('input',{})
        if not isinstance(ins,dict):
            errors.append(f'{node_id}: invalid supplied input schema');continue
        required=ins.get('required',{});optional=ins.get('optional',{})
        if not isinstance(required,dict) or not isinstance(optional,dict):
            warnings.append(f'{node_id}: unsupported input schema');continue
        defs={**required,**optional};values=node['inputs']
        for field in required:
            if field not in values:errors.append(f'{node_id}.{field}: required input missing')
        for field,value in values.items():
            label=f'{node_id}.{field}'
            if isinstance(value,float) and not math.isfinite(value):
                errors.append(label+': non-finite literal not supported');continue
            definition=defs.get(field)
            if definition is None:
                warnings.append(label+': not in declared required/optional schema; dynamic input not validated')
            kind=definition[0] if isinstance(definition,(list,tuple)) and definition else None
            opts=definition[1] if isinstance(definition,(list,tuple)) and len(definition)>1 and isinstance(definition[1],dict) else {}
            is_link=isinstance(value,list) and len(value)==2 and isinstance(value[0],(str,int)) and not isinstance(value[0],bool) and type(value[1]) is int
            if is_link:
                parent,index=str(value[0]),value[1]
                if parent not in graph:
                    errors.append(label+': link source does not exist: '+parent);continue
                if index<0:
                    errors.append(label+': output index must be nonnegative');continue
                links[node_id].append(parent)
                pnode=graph[parent];pschema=object_info.get(pnode.get('class_type'),{}) if isinstance(pnode,dict) else {}
                outputs=pschema.get('output') if isinstance(pschema,dict) else None
                if isinstance(outputs,list):
                    if index>=len(outputs):errors.append(label+': output index is out of range')
                    elif isinstance(kind,str) and isinstance(outputs[index],str) and kind not in {'*','ANY'} and outputs[index] not in {'*','ANY'} and kind!=outputs[index]:
                        errors.append(label+': declared link type mismatch '+outputs[index]+' -> '+kind)
                else:warnings.append(label+': source output schema unavailable')
                continue
            if opts.get('forceInput'):
                errors.append(label+': requires a connected input');continue
            if isinstance(kind,list):
                if value not in kind:errors.append(label+': value not in supplied environment choices')
            elif kind=='INT' and type(value) is not int:errors.append(label+': expected integer literal or link')
            elif kind=='FLOAT' and (not isinstance(value,(int,float)) or isinstance(value,bool)):errors.append(label+': expected numeric literal or link')
            elif kind=='STRING' and not isinstance(value,str):errors.append(label+': expected string literal or link')
            elif kind=='BOOLEAN' and type(value) is not bool:errors.append(label+': expected boolean literal or link')
            elif isinstance(kind,str) and kind not in {'INT','FLOAT','STRING','BOOLEAN','*','ANY'}:
                warnings.append(label+': opaque/custom literal not validated')
            if isinstance(value,(int,float)) and not isinstance(value,bool):
                for bound,op in [('min',lambda a,b:a<b),('max',lambda a,b:a>b)]:
                    if isinstance(opts.get(bound),(int,float)) and op(value,opts[bound]):errors.append(label+': outside '+bound+' constraint')
    # A simple dependency-cycle check; dynamic graph behavior still needs real execution.
    indegree={k:len(set(v)) for k,v in links.items()};reverse={k:[] for k in graph}
    for child,parents in links.items():
        for parent in set(parents):reverse[parent].append(child)
    stack=[k for k,n in indegree.items() if n==0];visited=0
    while stack:
        k=stack.pop();visited+=1
        for child in reverse[k]:
            indegree[child]-=1
            if indegree[child]==0:stack.append(child)
    if visited!=len(graph):errors.append('Dependency cycle detected; static checker requires an acyclic API graph.')
    return {'status':'static_issues' if errors else 'static_checks_passed','nodes':len(graph),
            'errors':errors,'warnings':warnings,'executed':False,
            'limitations':'Snapshot-based structural checks only; no server execution, tensor/device validation, model-file verification, memory test, license clearance or visual quality check.'}
