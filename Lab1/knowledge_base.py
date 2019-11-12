
features = {
    'класс': ['голосеменные', 'покрытосеменные'],
    'структура листа': ['чешуеобразная', 'иглободобная'],
    'семейство': ['кипарисовые', 'сосновые', 'еловые', 'болотный кипарис'],
    'конфигурация': ['хаотическая', 'два ровных ряда'],
    'серебристая полоса': ['нет', 'да'],
    'тип': ['деревья', 'травянистые', 'лианы', 'кустарниковые'],
    'форма листа': ['широкая и плоская', 'не широкая и плоская'],
    'стебель': ['зелёный', 'древесный'],
    'положение': ['прямостоящее', 'стелющееся'],
    '1 основной ствол': ['нет', 'да'],
}

features_to_ask = ['структура листа', 'форма листа', 'стебель', 'положение', '1 основной ствол']

kb = [
    ({'класс':'голосеменные', 'структура листа':'чешуеобразная'}, ('семейство','кипарисовые')),
    ({'класс':'голосеменные', 'структура листа':'иглободобная', 'конфигурация':'хаотическая'}, ('семейство','сосновые')),
    ({'класс':'голосеменные', 'структура листа':'иглободобная', 'конфигурация':'два ровных ряда'}, ('семейство','еловые')),
    ({'класс':'голосеменные', 'структура листа':'иглободобная', 'конфигурация':'два ровных ряда','серебристая полоса':'нет'}, ('семейство','болотный кипарис')),
    ({'тип': 'деревья', 'форма листа': 'широкая и плоская'}, ('класс', 'покрытосеменные')),
    ({'тип': 'деревья', 'форма листа': 'не широкая и плоская'}, ('класс', 'голосеменные')),
    ({'стебель': 'зелёный'}, ('тип', 'травянистые')),
    ({'стебель': 'древесный', 'положение': 'стелющееся'}, ('тип', 'лианы')),
    ({'стебель': 'древесный', 'положение': 'прямостоящее', '1 основной ствол': 'да'}, ('тип', 'деревья')),
    ({'стебель': 'древесный', 'положение': 'прямостоящее', '1 основной ствол': 'нет'}, ('тип', 'кустарниковые'))
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
