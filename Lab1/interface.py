from PyQt5 import uic
from PyQt5.QtWidgets import *

from knowledge_base import *


qtCreatorFile = "interface.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Interface(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.cb_target.addItems(features_res)
        self.pb_ask.clicked.connect(self.on_ask)
        self.pb_answer.clicked.connect(self.on_answer)
        self.pb_start.clicked.connect(self.start)

    def start(self):
        self.pb_start.setEnabled(False)
        self.label_target.setEnabled(True)
        self.cb_target.setEnabled(True)
        self.pb_ask.setEnabled(True)
        self.le_result.setText('')
        self.le_result.setEnabled(False)
        self.label_result.setEnabled(False)
        self.target_stack = []
        self.context_stack = []
        self.accepted_rules = []
        self.discarded_rules = []

    def on_ask(self):
        self.feature = self.cb_target.currentText()
        self.target_stack.append(self.feature)
        self.label_target.setEnabled(False)
        self.cb_target.setEnabled(False)
        self.pb_ask.setEnabled(False)

        self.algo()

    def algo(self):
        while len(self.target_stack) > 0:
            self.target_feature = self.target_stack[-1]
            rule_num = find_rule(self.target_feature, self.accepted_rules + self.discarded_rules)
            if rule_num > -1:
                rule_val, unknown_feature, feature_val = check_rule(rule_num, self.context_stack)
                if rule_val == True:
                    self.context_stack.append((self.target_feature, feature_val))
                    self.accepted_rules.append(rule_num)
                    self.target_stack.pop()
                elif rule_val == False:
                    self.discarded_rules.append(rule_num)
                else:
                    self.target_stack.append(unknown_feature)
            elif has_question(self.target_feature):
                q, ans = get_question(self.target_feature)
                self.label_question.setEnabled(True)
                self.label_question.setText(q)
                self.cb_answer.addItems(ans)
                self.cb_answer.setEnabled(True)
                self.pb_answer.setEnabled(True)
                return
            else:
                break

        self.le_result.setEnabled(True)
        self.label_result.setEnabled(True)
        self.pb_start.setEnabled(True)

        for f, v in self.context_stack:
            if self.feature == f:
                self.le_result.setText(v)
                return
        self.le_result.setText('Sorry, no answer was found')

    def on_answer(self):
        feature_val = self.cb_answer.currentText()
        self.context_stack.append((self.target_feature, feature_val))
        self.target_stack.pop()

        self.label_question.setText('')
        self.label_question.setEnabled(False)
        self.cb_answer.clear()
        self.cb_answer.setEnabled(False)
        self.pb_answer.setEnabled(False)

        self.algo()
