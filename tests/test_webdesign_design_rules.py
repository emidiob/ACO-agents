"""Behavioral examples and counterexamples for every design-review predicate."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/aco-webdesign/scripts'))
from design_rules import RULES

# Each tuple supplies an element that needs review and an ordinary counterexample.
CASES=[
({'borders':[4,0,0,0]},{'borders':[1,1,1,1]}),
({'radius':8,'borders':[4]},{'radius':0,'borders':[4]}),
({'fontFamily':'Inter, sans-serif'},{'fontFamily':'Georgia, serif'}),
({'tag':'h1','fontSize':18},{'tag':'h1','fontSize':36}),
({'backgroundClip':'text','backgroundImage':'linear-gradient(red,blue)'},{'backgroundClip':'border-box'}),
({'backgroundImage':'linear-gradient(rgb(0, 0, 255), rgb(0, 255, 255))'},{'backgroundImage':'none'}),
({'tag':'main','background':'#fff5e6'},{'tag':'main','background':'#ffffff'}),
({'radius':8,'borders':[1]},{'radius':0,'borders':[0]}),
({'tag':'main'},{'tag':'section'}),
({'timing':'cubic-bezier(.2,1.4,.8,1)'},{'timing':'cubic-bezier(.2,0,.8,1)'}),
({'width':8,'height':8,'animation':'pulse','animationDuration':'1s'},{'width':8,'height':8,'animation':'none'}),
({'text':'|','animation':'blink','animationDuration':'1s'},{'tag':'input','text':'|','animation':'blink','animationDuration':'1s'}),
({'tag':'svg','primitiveCount':20,'width':300},{'tag':'svg','primitiveCount':3,'width':300}),
({'clipPath':'path("M 0 0")'},{'clipPath':'circle(50%)'}),
({'tag':'img','opacity':.05},{'tag':'img','opacity':1}),
({'shadow':'rgb(0, 0, 0) 5px 5px 0px'},{'shadow':'rgb(0, 0, 0) 1px 2px 8px'}),
({'shadow':'rgb(255, 0, 0) 0px 0px 20px'},{'shadow':'rgb(20, 20, 20) 0px 0px 20px'}),
({'backgroundImage':'radial-gradient(rgb(255, 0, 0), rgb(0, 0, 255))'},{'backgroundImage':'linear-gradient(rgb(255, 0, 0), rgb(0, 0, 255))'}),
({'backgroundImage':'radial-gradient(red, transparent)'},{'backgroundImage':'none'}),
({'animation':'ticker','animationDuration':'10s'},{'animation':'none'}),
({'tag':'h2'},{'tag':'p'}),
({'tag':'h1','fontSize':64,'fontStyle':'italic','fontFamily':'Georgia, serif'},{'tag':'h1','fontSize':64,'fontStyle':'normal','fontFamily':'Georgia, serif'}),
({'tag':'h1'},{'tag':'p'}),
({'tag':'h2'},{'tag':'p'}),
({'text':'01','fontSize':10},{'text':'chapter','fontSize':10}),
({'text':'A sentence — '*9},{'text':'A sentence without long dashes.'}),
({'text':'Supercharge your workflow'},{'text':'Export invoices as CSV'}),
({'text':'Not this. No that. Just results.'},{'text':'Prepare three drafts.'}),
({'tag':'h1','fontSize':120,'text':'A long title with more than eight words here'},{'tag':'h1','fontSize':48,'text':'A long title with more than eight words here'}),
({'fontSize':16,'letterSpacing':-2},{'fontSize':16,'letterSpacing':0}),
({'tag':'img','src':'x.png','imageComplete':True,'naturalWidth':0},{'tag':'img','src':'x.png','imageComplete':True,'naturalWidth':100}),
({'tag':'body'},{'tag':'p'}),
({'text':'Hidden text '*10,'opacity':0,'display':'block'},{'text':'Visible text '*10,'opacity':1,'display':'block'}),
({'radius':8,'borders':[1],'left':0},{'radius':8,'borders':[1],'left':20}),
({'text':'Covered','occluded':True},{'text':'Visible','occluded':False}),
({'text':'Long text '*20,'top':0,'height':1000},{'text':'Short text','top':0,'height':100}),
({'text':'Neutral text','color':'#777777','effectiveBackground':'#ff0000'},{'text':'Neutral text','color':'#777777','effectiveBackground':'#ffffff'}),
({'text':'Low contrast','color':'#aaaaaa','effectiveBackground':'#ffffff'},{'text':'High contrast','color':'#000000','effectiveBackground':'#ffffff'}),
({'tag':'p','text':'Text '*40,'width':1000,'fontSize':16},{'tag':'p','text':'Text '*40,'width':500,'fontSize':16}),
({'text':'A long sentence in a framed box here','radius':8,'borders':[1],'padding':[0]},{'text':'A long sentence in a framed box here','radius':8,'borders':[1],'padding':[16]}),
({'tag':'p','text':'Paragraph '*10,'left':0,'right':500},{'tag':'p','text':'Paragraph '*10,'left':24,'right':500}),
({'tag':'p','fontSize':16,'lineHeightPx':16},{'tag':'p','fontSize':16,'lineHeightPx':24}),
({'headingGap':True},{'headingGap':False}),
({'tag':'h2','top':104},{'tag':'h2','top':130}),
({'tag':'p','textAlign':'justify'},{'tag':'p','textAlign':'start'}),
({'lineWidths':[200,190,20]},{'lineWidths':[200,190,150]}),
({'tag':'h1','lineWidths':[200,20]},{'tag':'h1','lineWidths':[200,150]}),
({'tag':'p','fontSize':10},{'tag':'p','fontSize':16}),
({'tag':'button','fontSize':10},{'tag':'button','fontSize':16}),
({'tag':'p','text':'LOUD TEXT '*15},{'tag':'p','text':'Normal text '*15}),
({'tag':'p','fontSize':16,'letterSpacing':3},{'tag':'p','fontSize':16,'letterSpacing':0}),
({'scrollWidth':300,'clientWidth':100,'overflowX':'hidden'},{'scrollWidth':300,'clientWidth':100,'overflowX':'auto'}),
({'text':'Repeated paragraph of enough length'},{'text':'Unique paragraph of enough length'}),
({'position':'absolute','left':-20,'right':300},{'position':'absolute','left':20,'right':300}),
({'fontFamily':'Arial'},{'fontFamily':'Georgia'}),
({'text':'Color','color':'#ff0000'},{'text':'Color','color':'#000000'}),
({'radius':11},{'radius':8}),
({'text':'Size','fontSize':17},{'text':'Size','fontSize':16}),
({'borders':[1],'shadow':'0px 4px 40px black'},{'borders':[1],'shadow':'0px 4px 8px black'}),
({'backgroundImage':'repeating-linear-gradient(red,blue)'},{'backgroundImage':'none'}),
({'backgroundImage':'linear-gradient(red,blue),linear-gradient(red,blue)','backgroundSize':'20px 20px'},{'backgroundImage':'linear-gradient(red,blue)','backgroundSize':'auto'}),
({'text':'The stage is set for your new project'},{'text':'Your project starts Monday'}),
]

class RuleExamples(unittest.TestCase):
    def test_positive_and_counterexample_for_each_rule(self):
        self.assertEqual(len(CASES),len(RULES))
        for i,((rule,_,_,predicate),(positive,negative)) in enumerate(zip(RULES,CASES)):
            with self.subTest(rule=rule):
                parent={'radius':8,'borders':[1],'overflowX':'hidden','left':0,'right':500,'display':'grid'}
                previous={'tag':'p','bottom':100,'hasIcon':True,'width':32,'radius':8,'text':'LABEL','fontSize':12,'letterSpacing':2}
                args=(parent,previous,{'scriptErrors':['test error']},{'fonts':['Georgia'],'colors':['#000000'],'radii':[8],'fontSizes':[16]},16,[20]*5,1200,800,['Repeated paragraph of enough length']*3)
                self.assertTrue(predicate(positive,*args),rule+' missed positive')
                self.assertFalse(predicate(negative,*args),rule+' flagged counterexample')
