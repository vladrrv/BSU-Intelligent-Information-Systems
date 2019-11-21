from collections import defaultdict

kb = [
    ({'данные размечены?': 'да'},
     ('характер обучения', 'с учителем')),

    ({'данные размечены?': 'нет', 'система взаимодействует со средой?': 'да'},
     ('характер обучения', 'с подкреплением')),

    ({'данные размечены?': 'нет', 'система взаимодействует со средой?': 'нет'},
     ('характер обучения', 'без учителя')),

    ({'есть обратные связи?': 'да'},
     ('класс сетей', 'рекуррентные')),

    ({'есть обратные связи?': 'нет', 'характер обучения': 'без учителя'},
     ('сеть', 'сеть Кохонена')),

    ({'есть обратные связи?': 'нет', 'характер обучения': 'с учителем'},
     ('класс сетей', 'сети прямого распространения')),

    ({'класс сетей': 'сети прямого распространения', 'каждый нейрон связан со всеми нейронами предыдущего слоя?': 'да'},
     ('сеть', 'персептрон')),
    ({'класс сетей': 'сети прямого распространения', 'каждый нейрон связан со всеми нейронами предыдущего слоя?': 'нет'},
    ('сеть', 'CNN')),

    ({'класс сетей': 'рекуррентные', 'есть вентили?': 'нет'},
     ('сеть', 'классическая RNN')),

    ({'класс сетей': 'рекуррентные', 'есть вентили?': 'да', 'количество вентилей': '3'},
     ('сеть', 'GRU')),

    ({'класс сетей': 'рекуррентные', 'есть вентили?': 'да', 'количество вентилей': '4'},
     ('сеть', 'LSTM')),

    ({'задача': 'вывод'},
     ('сеть', 'автоэнкодер')),

    ({'задача': 'генерация', 'сэмплинг из скрытого пространства': 'да'},
     ('сеть', 'автоэнкодер')),

    ({'задача': 'генерация', 'сэмплинг из скрытого пространства': 'нет'},
     ('сеть', 'GAN')),

    ({'задача': 'классификация', 'характер обучения': 'с учителем'},
     ('класс сетей', 'сети прямого распространения')),

    ({'задача': 'классификация', 'характер обучения': 'без учителя'},
     ('сеть', 'сеть адаптивного резонанса')),

    ({'задача': 'сжатие данных', 'характер обучения': 'с учителем'},
     ('класс сетей', 'сети прямого распространения')),

    ({'задача': 'сжатие данных', 'характер обучения': 'без учителя'},
     ('сеть', 'сеть Хопфилда'))
]


features = defaultdict(set)
features_res = set()
features_cause = set()
for causes, (f_res, v_res) in kb:
    features_res.add(f_res)
    features[f_res].add(v_res)
    for f, v in causes.items():
        features_cause.add(f)
        features[f].add(v)


features_to_ask = features_cause - features_res


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
    return str(feature).capitalize() + '? ', features[feature]
