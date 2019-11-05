
features = {
    0: ['a', 'b'],
    1: ['c', 'd'],
    2: ['e', 'f'],
}

features_to_ask = [0, 1]

kb = [
    ({0:'a'}, (1, 'd')),
    ({0:'a', 1:'d'}, (2, 'e')),
    ({0:'b', 1:'d'}, (2, 'f')),
]


def find_rule(feature, discarded_rules):
    for i in range(len(kb)):
        if i in discarded_rules:
            continue
        s, (f, v) = kb[i]
        if f == feature:
            return i
    return -1


def check_rule(rule_num, context):
    s, (f, v) = kb[rule_num]
    rule_val, unknown_feature = compare(context, s)
    return rule_val, unknown_feature, v


def compare(context, rule_conditions):

    # check if context does not contradict rule_conditions
    for f, v in context:
        for rf, rv in rule_conditions.items():
            if f == rf and v != rv:
                return False, None

    # check if context has all features from rule_conditions (if not, return first unknown rule)
    context_features = set([f for f,v in context])
    rule_features = set([f for f,v in rule_conditions.items()])
    dif = rule_features.difference(context_features)
    if len(dif) > 0:
        return None, next(enumerate(dif))[1]

    return True, None


def has_question(feature):
    return feature in features_to_ask


def get_question(feature):
    return str(feature) + '? - variants: ' + ', '.join(features[feature])
