# Current handover examples

Dated context from Erik and Mihkel's 18 November correspondence and the user's later initiation-letter examples. These are administrator/user statements to verify during setup. The letter supplied for the current invocation takes precedence over historical examples.

Source thread is [Uued VM-id](https://mail.google.com/mail/u/0/#all/1a1c01913819dab2). The skill contains a non-secret summary. Retrieve further correspondence only within the user's authorized scope. Leave one-time sudo-secret links for Erik to consume privately.

## Harald and three applications

Mihkel supplied `harald.arhiiv.ee`, accessible with the SSH public keys already registered on the Kaardid VM. He reports nginx, PHP 8.5 and PostgreSQL 18 installed. Erik accepted PostgreSQL 18. Managed `pgadmin4.arhiiv.ee` access is prepared.

The agreed capacity is 4 vCPU and 8 GB RAM, with one expandable OS disk chosen by Mihkel. Size all application pools plus PostgreSQL within that shared budget and inspect actual disk capacity.

| Project | Checkout | Internal hostname | Agreed public hostname |
| --- | --- | --- | --- |
| Tallinna aadresslehed | /Users/erikuus/dev/php/aadresslehed | aadresslehed.arhiiv.ee | aadresslehed.ra.ee |
| Pitserid | /Users/erikuus/dev/php/pitserid | pitserid.arhiiv.ee | pitserid.ra.ee |
| Nimeregister | /Users/erikuus/dev/php/nimeregister | nimeregister.arhiiv.ee | nimeregister.ra.ee |

Mihkel reports an existing certificate serving all three internal hostnames and initial reverse-proxy/Yii-oriented nginx files. Their proposed webroots are `/var/www/<app>/web`. Audit the files and mapping. Nimeregister is standalone PHP and needs its own entry-point/migration adapter. Reuse valid infrastructure and preserve sibling sites.

Nimeregister needs `fuzzystrmatch`. Aadresslehed and Pitserid need separate rehearsal/production databases with their discovered local/test equivalents. Inspect the existing repositories for current session handling, private config and media. Nimeregister's editable `content/` must survive deployment.

Mihkel says public hostnames await EEnet DNS records. Treat the stated internal sample sites and DNS progress as unverified live state until inspected. Final routing and public opening need current evidence.

## SOAP and iipsrv VM

The earlier 18 November planning email proposed 4 vCPU, 8 GB RAM and an expandable OS disk for `/Users/erikuus/dev/php/services` and iipsrv. The later supplied single-app initiation letter reports `teenused.arhiiv.ee`, user `erik`, SSH-key login, PHP-FPM 8.5, PostgreSQL 17, nginx, 8 vCPU, 16 GB RAM and 500 GB disk. For an invocation using that letter, use those newer reported values and verify them during the authorized audit.

The letter's visible hostname says `teenused.arhiiv.ee` while its hyperlink targets `kaardid.arhiiv.ee`. Resolve the canonical SSH target with the user/administrator before connecting and verify its independent host fingerprint/identity. Continue local project preparation while that input is pending. Preserve the agreed public identity `teenused.ra.ee` until a later explicit change, and verify final routing.

Services needs remote AIS/kmooduli PostgreSQL access, DGS and a persistent `/mnt/uuskasutus` file-server mount readable by PHP and iipsrv. The image collection stays on that file server. Discover optional ODBC/Imagick requirements from the repo and actual integrations.

Erik earlier said Services needs no local application database. A PostgreSQL 17 installation reported in the newer seed is administrator-provided infrastructure to preserve. Determine actual database needs from the application. Rehearsal/production still need separate code/private config/runtime/cache and safe remote-data usage.

The newer seed supplies initial access facts but does not establish a verified host fingerprint, archive export/mount details, external grants or public routing. Resolve each input before dependent work. Harald and local Codex project setup remain independent.

## Kaardid reference evidence

The reference repositories and Pages were inspected on 18 November 2026. Live `bin/vm status` at 17:25 UTC reported rehearsal HTTP 200, maintenance off in both environments, active production, three local deployment dumps in each environment and a timestamped successful scheduled updater completion.

Kaardid is already public and legacy homepage/deep-link redirects were verified during launch. The current policy uses manual dashboard refresh and three verified successful/resolved dumps plus unresolved attempts per environment. No new VM was provisioned while creating this skill.

Mihkel's correspondence describes whole-VM backups and separate DB backups. Record that confirmed policy and responsibility. Exact coverage, retention and restore evidence remain separate facts to establish.

Source examples are [Kaardid workflow](https://chatgpt.com/space/page_5874d65a5ab081919f2914584ef8be3a), [dashboard](https://chatgpt.com/space/page_206bb3e707788191b77360c2e206021d) and the reference source manifest bundled with this skill.

