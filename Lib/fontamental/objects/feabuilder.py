#!/usr/bin/env python
# encoding: utf-8

import os
import io


class FeaBuilder():

    options = {
        'hasLamAlefAlt': True,
        'hasMarkShaddaLeg': True,
    }
    fea_main = ''
    fea_classes = ''
    classes = {}

    def generateClasses(self):
        feaClasses = self._readFeaFile('classes.fea')
        feaClasses = feaClasses.split("\n")
        for classLine in feaClasses:
            if classLine.startswith('@'):
                classParts = classLine.split('=')
                className = classParts[0][1:]
                classUniMembers = classParts[1].replace('[','')
                classUniMembers = classUniMembers.replace(']', '')
                classUniMembers = classUniMembers.replace(';', '')
                classUniMembers = classUniMembers.split(' ')
                classMembers = self.getAvailable(classUniMembers)
                if len(classMembers) >= 1:
                    self._writeClasses({className:classMembers})
                    self.classes[className] = classMembers
        m = 1

    def getAvailable(self, gclass):
        try:
            available = []
            for gl in gclass:
                if gl in self.GDB.Decimal2Prod.values():
                    available.append(gl)
            return available
        except:
            pass

    def __init__(self, gdb, options=None):

        if options is not None:
            self.options = options


        self.lib_path = (os.sep).join((os.path.dirname(__file__).split(os.sep))[:-1])

        self.database_path = self.lib_path + '/database/'

        self.GDB = gdb

        self.generateClasses()

        self._createMainFea()

        self._createBasicArabic()

        if self.options['hasLamAlefAlt']:
            self._createLamAlef()

        if self.options['hasMarkShaddaLeg']:
            self._creatMarkShaddaLeg()
        self._setFeaClasses()

    def _createMainFea(self):
        """
        Main Features File, Contain general headers
        """
        self.fea_main += self._readFeaFile('main.fea')

    def _createBasicArabic(self):
        """
        Create the Classs to the basic arabic glyphs and there
        Presentations
        """
        FEA = {
            'init': [],
            'medi': [],
            'init_medi': [],
            'isol': [],
            'fina': [],
            'fina_isol': []
        }
        ar600 = sorted(self.GDB.Decimal2Prod.keys())
        for letter in ar600:
            if letter >= 1548 and letter <= 1784:
                blockName = self.GDB.Decimal2Prod[letter]
                mediName = blockName + '.medi'
                initName = blockName + '.init'
                isolName = blockName + '.isol'
                finaName = blockName + '.fina'
                if mediName in self.GDB.Decimal2Prod.values():
                    FEA['init_medi'].append(blockName)
                    FEA['medi'].append(mediName)
                    FEA['init'].append(initName)
                    assert initName in self.GDB.Decimal2Prod.values()
                    FEA['fina_isol'].append(blockName)
                    FEA['isol'].append(isolName)
                    assert isolName in self.GDB.Decimal2Prod.values()
                    FEA['fina'].append(finaName)
                    assert finaName in self.GDB.Decimal2Prod.values()
                elif finaName in self.GDB.Decimal2Prod.values():
                    FEA['fina_isol'].append(blockName)
                    FEA['isol'].append(isolName)
                    assert isolName in self.GDB.Decimal2Prod.values()
                    FEA['fina'].append(finaName)
                    assert finaName in self.GDB.Decimal2Prod.values()
        self._writeClasses(FEA)
        self.fea_main += self._readFeaFile('basic_ara.fea')



    def _createLamAlef(self):
        self.fea_main += self._readFeaFile('lamalef_ara.fea')

    def _creatMarkShaddaLeg(self):
        self.fea_main += self._readFeaFile('mk_shadda_ara.fea')

    def _setFeaClasses(self):
        self.fea_main = self.fea_main.replace('#include "classes.fea"', self.fea_classes)

    def _readFeaFile(self, feaFile):
        assert os.path.isfile(self.database_path + feaFile)
        with io.open(self.database_path + feaFile, 'r', encoding='utf-8') as f:
            return f.read()

    def _writeClasses(self, dict):
        for key in dict.keys():
            self.fea_classes += '@' + key
            self.fea_classes += " = [ " + " ".join(dict[key]) + " ];\n"
