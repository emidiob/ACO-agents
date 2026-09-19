"""Decimal project-estimate arithmetic, not accounting/tax advice or payments."""
from decimal import Decimal,InvalidOperation,ROUND_HALF_UP,localcontext
from .common import ACOError

def num(value,label):
    if isinstance(value,bool) or not isinstance(value,(str,int)):
        raise ACOError(label+': use a decimal string or integer, not a float/bool')
    if len(str(value))>80:raise ACOError(label+': numeric value is too long')
    try:v=Decimal(str(value))
    except InvalidOperation as e:raise ACOError(label+': invalid decimal') from e
    if not v.is_finite() or v<0:raise ACOError(label+': must be finite and nonnegative')
    if v>Decimal('1e12') or (v and v<Decimal('1e-8')):raise ACOError(label+': value outside supported estimate range')
    return v

def money(v):return str(v.quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
def pct(v):return str(v.quantize(Decimal('.0001'),rounding=ROUND_HALF_UP))

def budget_check(data):
    with localcontext() as context:
        context.prec=60
        try:return _budget_check(data)
        except InvalidOperation as e:raise ACOError("Calculation exceeds the supported precision") from e

def _budget_check(data):
    if not isinstance(data,dict):raise ACOError('Budget must be an object')
    currency=data.get('currency')
    if not isinstance(currency,str) or len(currency)!=3 or not currency.isalpha() or currency!=currency.upper():
        raise ACOError('Use one uppercase three-letter currency label; exchange rates are not inferred.')
    lines=data.get('lines')
    if not isinstance(lines,list) or not lines:raise ACOError('Provide nonempty cost lines')
    costs=Decimal(0);seen=set();items=[]
    for line in lines:
        if not isinstance(line,dict):raise ACOError('Cost line must be an object')
        key=line.get('id')
        if not isinstance(key,str) or not key or key in seen:raise ACOError('Each line needs a unique nonempty id')
        seen.add(key)
        if line.get('currency',currency)!=currency:raise ACOError('Mixed currencies require an explicit, sourced conversion before calculation')
        q=num(line.get('quantity'),'quantity');rate=num(line.get('unit_cost'),'unit_cost')
        total=q*rate;costs+=total
        items.append({'id':key,'quantity':str(q),'unit_cost':str(rate),'cost':money(total)})
    overhead=num(data.get('overhead','0'),'overhead')
    contingency_rate=num(data.get('contingency_percent','0'),'contingency_percent')
    if contingency_rate>100:raise ACOError('Contingency must be between 0 and 100 percent')
    base=costs+overhead;contingency=base*contingency_rate/100;total=base+contingency
    out={'status':'calculated','currency':currency,'lines':items,'direct_cost':money(costs),
         'overhead':money(overhead),'contingency':money(contingency),'total_cost':money(total),
         'basis':'Contingency applies to direct cost plus declared overhead. Profit here is before any unmodeled costs/taxes.',
         'executed_payment':False}
    if data.get('quote_net') is not None:
        quote=num(data['quote_net'],'quote_net');profit=quote-total
        out.update(quote_net=money(quote),estimated_contribution=money(profit),
                   margin_percent=pct(profit/quote*100) if quote else None,
                   markup_percent=pct(profit/total*100) if total else None)
    if data.get('target_margin_percent') is not None:
        target=num(data['target_margin_percent'],'target_margin_percent')
        if target>=100:raise ACOError('Target margin must be below 100 percent')
        out['price_for_target_margin']=money(total/(1-target/100))
    if data.get('tax_percent') is not None:
        tax=num(data['tax_percent'],'tax_percent')
        if data.get('quote_net') is None:raise ACOError('quote_net is required to apply a supplied tax rate')
        quote=num(data['quote_net'],'quote_net');out['tax_from_supplied_rate']=money(quote*tax/100)
        out['quote_including_supplied_tax']=money(quote*(1+tax/100))
        out['tax_note']='Supplied arithmetic assumption only; applicability not verified.'
    else:out['tax_note']='Tax not calculated; no rate or jurisdiction inferred.'
    return out
