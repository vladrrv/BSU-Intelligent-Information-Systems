from knowledge_base import *


def algo(feature):
    """
    Поместить конечную цель в стек целей.
    Логический признак = False

    while not логический признак:
        if можно найти правило для анализа:
            if значение правила == True:
                поместить целевой признак, его значение и
                номер анализируемого правила в стек контекста, и
                принять соответствующее правило.
                if стек целей пуст:
                    логический признак = True
                else:
                    рассматривать следующую цель из стека целей
            elif значение правила == False:
                поместить правило в колоду сброса.
            else:
                поместить первый неизвестный признак и номер соответствующего правила в стек целей
        elif имеется вопрос, связанный с текущей целью:
            задать вопрос.
            Поместить полученное значение в стек контекста вместе с признаком, удалив его из стека целей.
            if в стеке целей имеется номер правила:
                анализировать это правило (case).
        else:
            логический признак = True

    if конечная цель находится в стеке контекста:
        ответ получен.
    else:
        ответ не может быть найден.
    """
    target_stack = [feature]
    context_stack = []

    accepted_rules = []
    discarded_rules = []

    while len(target_stack) > 0:
        target_feature = target_stack[-1]
        rule_num = find_rule(target_feature, accepted_rules+discarded_rules)
        if rule_num > -1:
            rule_val, unknown_feature, feature_val = check_rule(rule_num, context_stack)
            if rule_val == True:
                context_stack.append((target_feature, feature_val))
                accepted_rules.append(rule_num)
                target_stack.pop()
            elif rule_val == False:
                discarded_rules.append(rule_num)
            else:
                target_stack.append(unknown_feature)
        elif has_question(target_feature):
            q = get_question(target_feature)
            feature_val = input(q)
            context_stack.append((target_feature, feature_val))
            target_stack.pop()
        else:
            break

    for f, v in context_stack:
        if feature == f:
            return v

    return None
