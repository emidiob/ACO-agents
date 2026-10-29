# ACO · Biblioteca di competenze

ACO **1.0.7**; metodi curati della biblioteca **0.3.0**, disponibili nell’uso ordinario.
Caricare solo la competenza pertinente e i metodi ACO già collegati. Le competenze non sono nuovi agenti. Ogni metodo dispone anche di una skill tecnica ACO 1.0.7 `professional.*` con status `validated` **esclusivamente per controlli procedurali sintetici**; rimangono non certificate professionalmente. Le 30 candidate tecniche precedenti non vengono promosse.

| Competenza | Uffici | Metodo |
|---|---|---|
| Critica visiva e web design | agency-office, product-office | [visual-critique](visual-critique/METHOD.md) |
| UX, ricerca utenti e servizi | product-office, agency-office, organization-office | [ux-research](ux-research/METHOD.md) |
| Accessibilità contestuale | product-office, agency-office, publishing-office | [accessibility](accessibility/METHOD.md) |
| Motion design delle interfacce | agency-office, product-office, production-office | [interface-motion](interface-motion/METHOD.md) |
| Video, montaggio e narrazione temporale | production-office, agency-office, publishing-office | [video-editing](video-editing/METHOD.md) |
| Genjutsu: osservazione e trasferimento del movimento | production-office, agency-office | [genjutsu-motion](genjutsu-motion/METHOD.md) |
| Ricerca curatoriale e costruzione di mostre | artist-office, organization-office | [curatorial-practice](curatorial-practice/METHOD.md) |
| Critica d’arte e sviluppo della pratica | artist-office, organization-office, publishing-office | [art-criticism](art-criticism/METHOD.md) |
| Archivi, opere e conservazione documentale | artist-office, organization-office, administration-office | [collections-records](collections-records/METHOD.md) |
| Marketing culturale e sviluppo del pubblico | organization-office, agency-office, artist-office | [cultural-marketing](cultural-marketing/METHOD.md) |
| Copywriting, contenuti e posizionamento | agency-office, commercial-office, publishing-office | [copy-positioning](copy-positioning/METHOD.md) |
| Giornalismo, editing e revisione documentale | publishing-office, administration-office, legal-office, agency-office | [editorial-verification](editorial-verification/METHOD.md) |
| Contratti, diritti e preparazione legale | legal-office, commercial-office, administration-office | [legal-review](legal-review/METHOD.md) |
| Amministrazione, segreteria e continuità operativa | administration-office, delivery-office | [administration](administration/METHOD.md) |
| Project management e consegna | delivery-office, agency-office, production-office | [project-delivery](project-delivery/METHOD.md) |
| Negoziazione, offerte e partnership | commercial-office, legal-office, artist-office | [negotiation](negotiation/METHOD.md) |
| Finanza di studio e controllo economico | finance-office, commercial-office, production-office | [studio-finance](studio-finance/METHOD.md) |
| HR, recruitment e sviluppo competenze | people-office, recruitment-office | [people-recruitment](people-recruitment/METHOD.md) |
| Strategia e valutazione dei programmi | organization-office, commercial-office, delivery-office | [strategy-evaluation](strategy-evaluation/METHOD.md) |
| Apprendimento e verifica delle competenze ACO | shared, product-office, delivery-office | [skill-evaluation](skill-evaluation/METHOD.md) |

## Uso nel checkout
```sh
python3 skills/aco-office-concierge/scripts/competence_library.py list --office artist-office
python3 skills/aco-office-concierge/scripts/competence_library.py show --id curatorial-practice
```

Il comando carica soltanto metodo, decisioni e contratto dell’output selezionato. Gli esempi e le fonti si leggono su richiesta. Non invoca un modello o un servizio esterno.

## Skill tecniche associate

Il registry `registry/skills.json` associa 20 nuove skill `professional.*` ai metodi qui elencati. Le skill vengono selezionate con il resolver ACO ordinario: `python3 scripts/aco_cli.py skill-search --query "curatorial exhibition thesis"`. I limiti di verifica sono documentati in [`docs/PROFESSIONAL-SKILLS.md`](../../../../docs/PROFESSIONAL-SKILLS.md).
