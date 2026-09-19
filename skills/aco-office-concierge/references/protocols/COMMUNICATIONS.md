# Communications and office actions

This is a host-executed protocol, not a bundled messaging/phone service. ACO remains a skill library, not a plugin. Connected apps/MCPs are optional and independently authorized.

## Capability check before promising an action
1. Identify the requested action and channel, sending identity, target and task scope. Read the relevant complete thread or authorized record first. Do not search unrelated correspondence.
2. Inspect tools already available. Discover app/MCP actions by their actual schema. If the capability is missing and discovery is available, search once for the relevant provider/capability. Suggest a connection only when useful; do not require an app just to draft.
3. Verify the particular operation: read email != create draft != send; read call logs != place a call; WhatsApp text send != WhatsApp voice calling; TTS != telephony; publishing draft != publishing live.
4. Resolve the contact from authorized Contacts/provider evidence. Verify account and exact recipient/chat/group/event IDs. Do not infer a destination from a name, a past conversation in another project, a phone suffix or a similarly named contact.
5. Verify the approved content/objective, CC/BCC, attachments/links, scope, time and costs. Reuse explicit authorization already given for this exact action; do not ask twice. Clarify ambiguity before action. Scoped recurring authorization requires an actual authorized scheduler/event runner and still obeys host permission rules.
6. Check prior action/session/provider evidence for duplicates. Call only the exact supported action. Never switch providers/endpoints to bypass a denied action or silently switch channels.
7. Record the provider reference and exact outcome. A successful request can mean accepted/queued, not delivered/read/answered. On timeout or uncertain response, mark OUTCOME UNKNOWN and reconcile before retrying.

## Email
Read full relevant thread. Resolve reply-all vs reply, sending account, recipients and attachments. Send only with explicit authority. An editable draft in Gmail is a separate write from a draft shown in chat. Do not forward full private context unnecessarily.

## WhatsApp / WhatsApp MCP
Use a user-connected and authorized MCP only if actual exposed actions support the request. Verify the recipient or group through the provider and preserve its returned identifier. Text/media/group membership/voice are separate actions. Inspect bridge health when supported; unavailable tunnel/bridge means NOT SENT. Never infer that a remembered bridge is available now. No unsolicited mass messaging or adding contacts/groups without permission. If a send might already have been accepted, do not issue it again blindly.

## Voice calls
Require actual outbound-calling capability, the verified number, identity to present, purpose, language, allowed disclosures, timing/timezone and boundaries on commitments. For AI-assisted calls disclose that an assistant is acting on the user’s behalf; do not impersonate a real person. Do not claim an answered conversation from a queued call request. Recording/transcription needs separate consent and applicable-rule checks. No emergency calling workflow; direct the user to appropriate local emergency services when urgent. A phone plugin name or a call history record is not evidence that outbound calls exist.

## Calendar, travel and purchases
Read availability before booking. Creating invitations, changing attendees, spending, subscriptions and travel purchases are distinct external actions. A plan is not a booking. No default financial commitments.

## Ready-to-copy fallback
When tools are absent or read-only, return the useful material immediately:
- Email: To / Cc if relevant / Subject / Body / intended attachments.
- WhatsApp/SMS: verified destination if known / message only / attachment notes.
- Phone: number if verified / short opening / purpose / questions / authorized limits / voicemail version.
- Meeting: title / participants / proposed date and timezone / agenda.
Label NOT SENT, NOT CALLED, NOT BOOKED or NOT PUBLISHED once, outside the copyable body. Do not put operational chatter in the message the user will paste. Do not auto-connect services or collect tokens/passwords in chat.

## History and confidentiality
Keep action ID, scope, channel, time, target reference, content fingerprint and minimal receipt in private project history. Do not place private phone numbers, HR matters, legal text, access tokens, message contents or Drive IDs in the public repo. The local action-plan helper validates a packet's shape/declared assertions only; it does not prove real authorization and never sends anything.
