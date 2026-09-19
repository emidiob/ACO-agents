import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError
from aco.planning import intake,plan_action,action_fingerprint

class IntakeTests(unittest.TestCase):
 def test_early_questions(self):
  r=intake('comfyui',{});self.assertEqual(r['status'],'needs_clarification');self.assertEqual(len(r['questions']),3)
 def test_answered_questions_not_repeated(self):
  r=intake('comfyui',{'goal':'fix artifact','environment':'known'});self.assertEqual([x['key'] for x in r['questions']],['assets'])
 def test_unknown_does_not_pass(self):
  self.assertEqual(intake('comfyui',{'goal':'TBD'})['status'],'needs_clarification')
 def test_no_questions_for_known_brief(self):
  r=intake('comfyui',{'goal':'repair','environment':'local','assets':'supplied'});self.assertEqual(r['questions'],[]);self.assertFalse(r['executed'])
 def test_no_global_client_assumption(self):
  self.assertIn('scope',[q['key'] for q in intake('email',{})['questions']])
 def test_action_default(self):self.assertEqual(intake('email',{})['mode'],'ACTION')
 def test_explain_allowed(self):self.assertEqual(intake('email',{},mode='EXPLAIN')['mode'],'EXPLAIN')
 def test_invalid_mode(self):
  with self.assertRaises(ACOError):intake('email',{},mode='verbose')
 def test_unknown_workflow(self):
  with self.assertRaises(ACOError):intake('unknown',{})
 def test_invalid_facts(self):
  with self.assertRaises(ACOError):intake('email',[])

class ActionTests(unittest.TestCase):
 def setUp(self):
  self.req={'action_id':'example-action','scope_id':'example-project','channel':'whatsapp','operation':'send_message','intent':'execute','account_id':'example-account','target_id':'example-contact','body':'Test message','recipient_verified':True}
  self.cap={'available':True,'connected':True,'schema_verified':True,'operations':['send_message'],'account_id':'example-account'}
  self.auth={k:self.req[k] for k in ('action_id','scope_id','channel','operation','account_id','target_id')}
  self.auth.update(reference='explicit-test-approval',content_sha256=action_fingerprint(self.req))
 def test_no_tool_gives_copy_ready(self):self.assertEqual(plan_action(self.req)['status'],'copy_ready_not_executed')
 def test_available_not_connected(self):
  self.cap['connected']=False;self.assertEqual(plan_action(self.req,self.cap)['status'],'copy_ready_not_executed')
 def test_schema_unverified(self):
  self.cap['schema_verified']=False;self.assertEqual(plan_action(self.req,self.cap)['status'],'copy_ready_not_executed')
 def test_read_only_not_send(self):
  self.cap['operations']=['read_messages'];self.assertEqual(plan_action(self.req,self.cap)['status'],'copy_ready_not_executed')
 def test_denied_does_not_try_alternate(self):
  self.cap['denied']=True;self.assertEqual(plan_action(self.req,self.cap)['status'],'blocked')
 def test_authorization_required(self):self.assertEqual(plan_action(self.req,self.cap)['status'],'awaiting_authorization')
 def test_exact_authorization_can_prepare(self):
  r=plan_action(self.req,self.cap,self.auth);self.assertEqual(r['status'],'ready_for_host_action');self.assertFalse(r['executed'])
 def test_changed_recipient_invalidates_approval(self):
  self.req['target_id']='another-contact';self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'awaiting_authorization')
 def test_changed_message_invalidates_approval(self):
  self.req['body']='changed';self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'awaiting_authorization')
 def test_changed_attachments_invalidates_approval(self):
  self.req['attachments']=['private-draft'];self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'awaiting_authorization')
 def test_cross_scope_approval_not_reused(self):
  self.auth['scope_id']='other-project';self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'awaiting_authorization')
 def test_sender_mismatch(self):
  self.cap['account_id']='other-account';self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'needs_clarification')
 def test_unverified_contact_asks(self):
  self.req['recipient_verified']=False;self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'needs_clarification')
 def test_ambiguous_timeout_no_duplicate(self):
  self.assertEqual(plan_action(self.req,self.cap,self.auth,{'status':'timeout'})['status'],'reconcile_before_retry')
 def test_already_accepted_no_duplicate(self):
  self.assertEqual(plan_action(self.req,self.cap,self.auth,{'status':'accepted'})['status'],'reconcile_before_retry')
 def test_sent_no_duplicate(self):
  self.assertEqual(plan_action(self.req,self.cap,self.auth,{'status':'sent'})['status'],'reconcile_before_retry')
 def test_draft_never_sends(self):
  self.req['intent']='draft';r=plan_action(self.req,self.cap,self.auth);self.assertEqual(r['status'],'draft_only');self.assertFalse(r['host_action_eligible'])
 def test_calls_not_inferred_from_logs(self):
  self.req.update(channel='phone',operation='place_call');self.cap['operations']=['read_call_logs']
  self.assertEqual(plan_action(self.req,self.cap)['status'],'copy_ready_not_executed')
 def test_calls_need_disclosure_and_limits(self):
  self.req.update(channel='phone',operation='place_call');self.cap['operations']=['place_call']
  r=plan_action(self.req,self.cap);self.assertEqual(r['status'],'needs_clarification');self.assertIn('ai_disclosure',r['missing'])
 def test_whatsapp_send_not_voice(self):
  self.req['operation']='place_call'
  with self.assertRaises(ACOError):plan_action(self.req,self.cap,self.auth)
 def test_invalid_input(self):
  with self.assertRaises(ACOError):plan_action([])
 def test_unknown_channel(self):
  self.req['channel']='unsupported'
  with self.assertRaises(ACOError):plan_action(self.req)
 def test_packet_not_mutated(self):
  before=copy.deepcopy(self.req);plan_action(self.req,self.cap,self.auth);self.assertEqual(before,self.req)

 def test_capability_operations_not_string(self):
  self.cap['operations']='send_message'
  with self.assertRaises(ACOError):plan_action(self.req,self.cap,self.auth)
 def test_identifier_wrong_type(self):
  self.req['target_id']=1
  with self.assertRaises(ACOError):plan_action(self.req,self.cap,self.auth)
 def test_action_id_required_for_execution(self):
  del self.req['action_id'];self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'needs_clarification')
 def test_approval_action_id_bound(self):
  self.auth['action_id']='another-action';self.assertEqual(plan_action(self.req,self.cap,self.auth)['status'],'awaiting_authorization')
