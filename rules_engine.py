import rules
from dataclasses import dataclass
import re
from enum import StrEnum


@dataclass
class RequestFact:
    chrome_extension_id: str

@rules.predicate
def has_one_extension_id(req: RequestFact):
    return req.chrome_extension_id is not None and len(re.split(r"[\s,]+", req.chrome_extension_id)) == 1

@rules.predicate
def has_valid_chrome_extension_id(req: RequestFact):
    # validate extension id
    return True

has_one_valid_chrome_extension_id = has_one_extension_id & has_valid_chrome_extension_id

class RuleResult(StrEnum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

class RulesEngine:
    def __init__(self):
        self.rule_set = rules.RuleSet()
        self.rule_names = []
    
    def add_rule(self, name, predicate):
        self.rule_names.append(name)
        self.rule_set.add_rule(name, predicate)

    def run_all(self, fact) -> dict[str,RuleResult]:
        results = {}
        for name in self.rule_names:
            match self.rule_set.test_rule(name, fact):
                case None:
                    results[name] = RuleResult.SKIPPED
                case True:
                    results[name] = RuleResult.PASSED
                case False:
                    results[name] = RuleResult.FAILED
        return results
            


if __name__ == "__main__":
    rules_engine = RulesEngine()
    rules_engine.add_rule("Has Valid Chrome Extension ID", has_one_valid_chrome_extension_id)
    fact = RequestFact(chrome_extension_id="123")
    results = rules_engine.run_all(fact)
    print("Valid Fact:")
    for name,res in results.items():
        print(f"{name} -> {res}")

    invalid_fact = RequestFact(chrome_extension_id="123, 456")
    results2 = rules_engine.run_all(invalid_fact)
    print("Invalid Fact:")
    for name,res in results2.items():
        print(f"{name} -> {res}")

