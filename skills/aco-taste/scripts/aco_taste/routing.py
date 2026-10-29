"""ACO original medium-aware automatic taste selection. No source text or vendor code."""
from __future__ import annotations
import re

VISUAL_TERMS = {
    'web': ('website','webdesign','landing','homepage','html','css','frontend','web page','sito','pagina web','portfolio website'),
    'ui': ('user interface','ui','ux','dashboard','app screen','component','interfaccia','prototip','design system','figma','mobile app'),
    'photo': ('photograph','photo','photoshoot','fotografi','foto','ritratto','still life','editorial shoot','comfyui','image prompt','nanobanana','seedream'),
    'image': ('image','images','immagine','immagini','poster','graphic','graphic design','grafica','logo','brand identity','visual identity','illustrazion','artwork','render','visual'),
    'video': ('video','film','footage','cinematograph','montaggio','montare','seedance','genjutsu','storyboard','scene','clip','reel','short film','animatic'),
    'motion': ('motion','animation','animazione','transizione','gsap','remotion','after effects','microinteraction','effetti visivi','vfx'),
    'document': ('presentation','slide','deck','pitch deck','brochure','magazine','catalog','publication','pdf design','layout','impaginazione','editorial design','poster print','typography','tipografia','book design'),
    'spatial': ('3d','spatial','exhibition design','installation','allestimento','scenography','set design','environment design','product render'),
}
ACTION = ('change','update','cambia','aggiorna','design','create','draw','make','build','generate','edit','revise','polish','improve','fix','review','critique','redesign','animate','render','produce','write prompt','shoot','shooting','compose','rework','resize','restyle','layout','impagin','crea','fai','progetta','rived','modifica','migliora','correggi','genera','disegna','realizza','monta','anima','fotografa','valuta','critica','risistema','ritocca','sviluppa','testa')
REVIEW=('critique','review','audit','valuta','critica','rived','analiz','inspect','esamina','controlla','check')
MINOR=('only the','just change','only change','solo ','soltanto ','quick fix','typo','one pixel','singola correzione','small change','one color','un colore','solo il testo','cambia solo')

PROFILES={
 'web':('reference-and-project-evidence','subject-led-direction','visual-build','browser-screenshot-review','accessibility-and-responsive','compare-before-after'),
 'ui':('reference-and-project-evidence','product-task-and-design-system','visual-build','interactive-state-review','keyboard-and-responsive','compare-before-after'),
 'photo':('reference-and-project-evidence','photographic-art-direction','capture-light-matter-and-composition','actual-image-review','series-consistency-and-rights'),
 'image':('reference-and-project-evidence','graphic-or-image-direction','visual-production','actual-image-or-layout-review','typography-and-assets-rights'),
 'video':('reference-and-project-evidence','cinematic-art-direction','shot-action-timeline','frame-contact-sheet-and-playback-review','movement-and-continuity'),
 'motion':('reference-and-project-evidence','motion-intention','behavior-and-timing','actual-motion-review','reduced-motion-and-performance'),
 'document':('reference-and-project-evidence','editorial-art-direction','typographic-hierarchy-and-grid','page-render-review','print-or-export-readability'),
 'spatial':('reference-and-project-evidence','spatial-art-direction','scale-light-material','render-or-photo-review','spatial-and-technical-consistency'),
}

def classify(task:str, *,declared_medium:str|None=None,operation:str|None=None,force_visual:bool=False):
    """Return visual routing based on user task intent, never treat discussion alone as action.

    Explicit medium is authoritative for the active task; a text question about an image
    doesn't obligate generation. Certain action verbs force pre/post gates.
    """
    if not isinstance(task,str):raise ValueError('task must be string')
    s=' '+task.lower()+' '
    explicit=(declared_medium or '').strip().lower()
    if explicit and explicit not in PROFILES:raise ValueError('Unsupported medium: '+explicit)
    scores={key:sum(bool(re.search(r'(?<![a-z])'+re.escape(term)+r'(?![a-z])',s)) for term in terms) for key,terms in VISUAL_TERMS.items()}
    if explicit:scores[explicit]=100
    dominant=sorted(scores,key=lambda x:(-scores[x],list(PROFILES).index(x)))[0]
    is_action=force_visual or bool(operation in {'create','edit','review','generate','polish','produce','redesign'}) or any(x in s for x in ACTION)
    triggered=bool(sum(scores.values())) and is_action
    if force_visual and not any(scores.values()):dominant=explicit or 'image';triggered=True
    mode='focused-edit' if any(x in s for x in MINOR) else 'review-only' if operation=='review' or (any(x in s for x in REVIEW) and not any(x in s for x in ('fix','change','modify','modifica','correggi','migliora','redesign','improve','build','make','create'))) else 'full'
    procedures=list(PROFILES[dominant]) if triggered else []
    if mode=='focused-edit' and triggered:procedures=['respect-locked-identity','apply-exact-user-change','inspect-changed-region-and-regressions']
    if mode=='review-only' and triggered:procedures=['read-brief-and-identity','inspect-actual-evidence','rank-specific-findings','do-not-mutate-without-permission']
    return {'automatic_taste':triggered,'medium':dominant if triggered else None,'mode':mode if triggered else 'not-applicable','workflow':procedures,'stage':'direction+production+review' if triggered else 'not-visual-work','preferred_review':'different reviewer if independent host/tool exists; otherwise separate skeptical pass with evidence','skip_rule':'Never skip visual gate on a visual deliverable; a focused edit uses proportional inspection, not full rebranding','role_policy':'Reuse existing ACO office/role; taste is a mandatory cross-office quality layer, not another office','unavailable_evidence':'Do not claim verified quality when images, playback or browser rendering were not inspected'}
