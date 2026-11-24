import copy, hashlib, json, tempfile, unittest
from pathlib import Path
from check_contract import inspect_plan

class ContractTests(unittest.TestCase):
    def plan(self):
        return json.loads((Path(__file__).resolve().parents[1]/'examples/contract.json').read_text(encoding='utf-8'))
    def test_valid_example_is_not_modified(self):
        d=self.plan();before=copy.deepcopy(d)
        self.assertTrue(inspect_plan(d)['contract_valid'])
        self.assertEqual(d,before)
    def test_foreign_role_and_malformed_input_are_rejected(self):
        d=self.plan();d['skill']='foreign-skill'
        self.assertFalse(inspect_plan(d)['contract_valid'])
        for bad in [None,[],{},'text',{'skill':self.plan()['skill']}]:
            self.assertFalse(inspect_plan(bad)['contract_valid'])

    def test_bad_source_speed_or_reference_does_not_pass(self):
        d=self.plan();d['clips'][0]['speed']=2
        self.assertFalse(inspect_plan(d)['contract_valid'])
        d=self.plan();d['clips'][0]['source_out']=101
        self.assertFalse(inspect_plan(d)['contract_valid'])
        d=self.plan();d['commentary'][0]['source_clip_ids']=['missing']
        self.assertFalse(inspect_plan(d)['contract_valid'])
    def test_opinion_is_not_required_to_masquerade_as_plot_fact(self):
        d=self.plan();d['commentary'][0].update(type='opinion',source_clip_ids=[])
        self.assertTrue(inspect_plan(d)['contract_valid'])


    def test_explicit_spoiler_cutoff_is_enforced_on_source_clock(self):
        d=self.plan();d['spoiler_source_limit']=25
        self.assertFalse(inspect_plan(d)['contract_valid'])
        d['spoiler_source_limit']=30
        self.assertTrue(inspect_plan(d)['contract_valid'])

if __name__=='__main__': unittest.main()
