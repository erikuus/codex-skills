# Upgrade Sources (Official)

Use these sources as the canonical baseline when preparing or validating the upgrade plan.

## Yii

- Yii 1.1 changelog (1.1.32 tag):
  - https://github.com/yiisoft/yii/blob/1.1.32/CHANGELOG
- Yii UPGRADE notes:
  - https://raw.githubusercontent.com/yiisoft/yii/1.1.32/UPGRADE

Focus points from UPGRADE for old 1.1.x apps:
- validator instantiation behavior (`CModel::createValidators`, since 1.1.11)
- migration transaction semantics (`CDbMigration::safeUp/safeDown`, since 1.1.13)
- active input ID/name behavior (`CHtml::activeId`, since 1.1.13)
- `CGridView` URL manager/path format interaction (since 1.1.14)

## PHP

- PHP migration guides (official manual):
  - https://www.php.net/manual/en/migration70.incompatible.php
  - https://www.php.net/manual/en/migration71.incompatible.php
  - https://www.php.net/manual/en/migration72.incompatible.php
  - https://www.php.net/manual/en/migration80.incompatible.php
  - https://www.php.net/manual/en/migration81.incompatible.php
  - https://www.php.net/manual/en/migration82.incompatible.php
  - https://www.php.net/manual/en/migration83.incompatible.php
  - https://www.php.net/manual/en/migration84.incompatible.php

## jQuery / jQuery UI

- jQuery Core upgrade guidance:
  - https://jquery.com/upgrade-guide/1.9/
- jQuery UI upgrade guides:
  - https://jqueryui.com/upgrade-guide/1.9/
  - https://jqueryui.com/upgrade-guide/1.10/
  - https://jqueryui.com/upgrade-guide/1.11/
  - https://jqueryui.com/upgrade-guide/1.12/

## PostgreSQL (if in same project window)

- Version 17 release notes:
  - https://www.postgresql.org/docs/17/release-17.html
- Upgrade tooling (`pg_upgrade`):
  - https://www.postgresql.org/docs/17/pgupgrade.html
- Prior major release notes (11-16):
  - https://www.postgresql.org/docs/11/release-11.html
  - https://www.postgresql.org/docs/12/release-12.html
  - https://www.postgresql.org/docs/13/release-13.html
  - https://www.postgresql.org/docs/14/release-14.html
  - https://www.postgresql.org/docs/15/release-15.html
  - https://www.postgresql.org/docs/16/release-16.html

