# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, print_function, division

from coh.tools.tag import *
from coh.tools.parse import *
from coh.tools.dependency import *
from coh.tools.lsa import *

pos_tagger = NLPNetTagger()
univ_pos_tagger = OpenNLPUniversalTagger()
parser = LxParser()
dep_parser = MaltParser(tagger=univ_pos_tagger)

from coh.tools.tokenizers import senter, word_tokenize
from coh.tools.syllable import *
from coh.tools.stemmers import DelafStemmer

stemmer = DelafStemmer()
