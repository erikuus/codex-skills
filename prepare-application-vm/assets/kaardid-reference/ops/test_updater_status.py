#!/usr/bin/env python3
"""Exercise the read-only updater status without touching installed units or databases."""
from datetime import datetime
import json
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
import unittest

status = runpy.run_path(str(Path(__file__).with_name('vm-status.py')))
missed = status['missed_updater_run']
read_history = status['updater_history']


class UpdaterStatusTest(unittest.TestCase):
    def setUp(self):
        # After the spring daylight-saving shift, 04:00 Tallinn is 01:00 UTC.
        self.due = int(datetime.fromisoformat('2026-03-29T01:00:00+00:00').timestamp())
        self.timer = dict(ActiveState='active', ActiveEnterTimestamp=f'@{self.due-7200}',
                          TimersCalendar='{ OnCalendar=*-*-* 04:00:00 Europe/Tallinn ; next_elapse=@0 }')

    def test_due_slot_without_trigger(self):
        self.assertIsNone(missed(self.timer, {}, None, self.due+5*60))
        self.assertEqual(missed(self.timer, {}, None, self.due+16*60),
                         {'at':self.due,'stage':'trigger'})
        self.timer['ActiveEnterTimestamp'] = f'@{self.due+1000}'
        self.assertIsNone(missed(self.timer, {}, None, self.due+1800))
        self.timer.update(ActiveState='inactive', ActiveEnterTimestamp=f'@{self.due-7200}')
        self.assertIsNone(missed(self.timer, {}, None, self.due+2400))

    def test_trigger_without_completion(self):
        self.timer['LastTriggerUSec'] = f'@{self.due+60}'
        self.assertIsNone(missed(self.timer, {}, None, self.due+2*3600))
        after_deadline = self.due+3*3600
        self.assertEqual(missed(self.timer, {}, None, after_deadline),
                         {'at':self.due,'stage':'completion'})
        self.assertIsNone(missed(self.timer, {}, {'startedAt':self.due+60}, after_deadline))
        failed = dict(Result='timeout', StateChangeTimestamp=f'@{self.due+7200}')
        self.assertIsNone(missed(self.timer, failed, None, after_deadline))

    def test_supervised_run_does_not_cover_a_missing_trigger(self):
        self.assertEqual(missed(self.timer, {}, None, self.due+3600)['stage'], 'trigger')

    def test_history_distinguishes_missing_invalid_and_zero(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)/'updater-runs.json'
            self.assertEqual(read_history(path)['historyStatus'], 'empty')
            path.write_text('{broken')
            self.assertEqual(read_history(path)['historyStatus'], 'unavailable')
            counts = dict.fromkeys(('dgsPages','mapsAdded','imagesAdded','imagesRemoved',
                                   'thumbnailsSaved','thumbnailFailures'), 0)
            counts['thumbnailFailures'] = 1
            run = dict(source='timer', outcome='warning', stage='thumbnails',
                       startedAt=self.due, finishedAt=self.due+30, intervalFrom=self.due-86400,
                       checkpointAfter=self.due, counts=counts, forbidden='private row')
            path.write_text(json.dumps(dict(version=1, runs=[run], lastScheduledRun=run,
                                            noAdditionsStreak=12, lastAdditionAt=None)))
            status = read_history(path)
            self.assertEqual(status['noAdditionsStreak'], 12)
            self.assertEqual(status['lastScheduledRun']['counts'], counts)
            self.assertNotIn('forbidden', status['runs'][0])
            alias = path.with_name('alias')
            alias.symlink_to(path)
            self.assertEqual(read_history(alias)['historyStatus'], 'unavailable')


if __name__ == '__main__':
    unittest.main()
