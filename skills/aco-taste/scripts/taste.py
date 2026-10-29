#!/usr/bin/env python3
"""ACO Taste CLI. Structured visual work; no direct model or provider execution."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from aco_taste import routing,core,directions,review,system,compare
import argparse,json

def read_packet(path):
    obj=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(obj,dict):raise ValueError('Packet must be JSON object')
    return obj

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    cmds=ap.add_subparsers(dest='command',required=True)
    rt=cmds.add_parser('route');rt.add_argument('--task',required=True);rt.add_argument('--medium',choices=list(routing.PROFILES));rt.add_argument('--operation');rt.add_argument('--force-visual',action='store_true')
    dr=cmds.add_parser('directions');dr.add_argument('--brief',required=True);dr.add_argument('--count',type=int,default=3);dr.add_argument('--seed',type=int,default=0)
    col=cmds.add_parser('collection-new');col.add_argument('--project',required=True);col.add_argument('--name',required=True);col.add_argument('--description',default='')
    ref=cmds.add_parser('reference-add');ref.add_argument('--project',required=True);ref.add_argument('--collection',required=True);ref.add_argument('--url');ref.add_argument('--file');ref.add_argument('--note',default='');ref.add_argument('--role',default='inspiration',choices=['inspiration','direction','negative','constraint']);ref.add_argument('--negative',action='store_true')
    fb=cmds.add_parser('feedback-add');fb.add_argument('--project',required=True);fb.add_argument('--variant',required=True);fb.add_argument('--judgment',required=True,choices=['prefer','reject','both','neither','depends','approve','revision']);fb.add_argument('--reason',required=True);fb.add_argument('--scope',default='current-project');fb.add_argument('--aspect',action='append',default=[])
    ins=cmds.add_parser('insights');ins.add_argument('--project',required=True);ins.add_argument('--scope',default='current-project')
    st=cmds.add_parser('status');st.add_argument('--project',required=True)
    ga=cmds.add_parser('gate');ga.add_argument('--packet',required=True)
    au=cmds.add_parser('audit-css');au.add_argument('--file',required=True)
    au=cmds.add_parser('audit-html');au.add_argument('--file',required=True)
    pf=cmds.add_parser('media-preflight');pf.add_argument('--file',required=True)
    sy=cmds.add_parser('design-md');sy.add_argument('--packet',required=True);sy.add_argument('--project',required=True);sy.add_argument('--apply',action='store_true')
    co=cmds.add_parser('compare');co.add_argument('--packet',required=True);co.add_argument('--output',required=True)
    ca=cmds.add_parser('catalog')
    args=ap.parse_args(argv)
    try:
        if args.command=='route':out=routing.classify(args.task,declared_medium=args.medium,operation=args.operation,force_visual=args.force_visual)
        elif args.command=='directions':out=directions.propose(read_packet(args.brief),count=args.count,seed=args.seed)
        elif args.command=='collection-new':out=core.new_collection(core.project_root(args.project),args.name,args.description)
        elif args.command=='reference-add':out=core.add_reference(core.project_root(args.project),args.collection,url=args.url,file=args.file,note=args.note,role=args.role,negative=args.negative)
        elif args.command=='feedback-add':out=core.add_feedback(core.project_root(args.project),args.variant,args.judgment,args.reason,scope=args.scope,aspects=args.aspect)
        elif args.command=='insights':out=core.insights(core.project_root(args.project),scope=args.scope)
        elif args.command=='status':out=core.status(core.project_root(args.project))
        elif args.command=='gate':out=review.evidence_gate(read_packet(args.packet))
        elif args.command=='audit-css':out=review.audit_css(Path(args.file).read_text(encoding='utf-8'))
        elif args.command=='audit-html':out=review.audit_html(Path(args.file).read_text(encoding='utf-8'))
        elif args.command=='media-preflight':out=review.media_preflight(args.file)
        elif args.command=='design-md':out=system.write_design_md(args.project,read_packet(args.packet),apply=args.apply)
        elif args.command=='compare':out=compare.write_board(read_packet(args.packet),args.output)
        else:out={'original_materials':directions.catalog(),'source':'ACO-original, not Hallmark code/themes'}
        print(json.dumps(out,indent=2,ensure_ascii=False))
        return 0
    except (OSError,ValueError,KeyError) as e:
        print(json.dumps({'status':'error','error':str(e)},ensure_ascii=False),file=sys.stderr)
        return 1
if __name__=='__main__':raise SystemExit(main())
