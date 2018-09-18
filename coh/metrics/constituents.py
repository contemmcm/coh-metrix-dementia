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
from coh import base
from coh.resource_pool import rp as default_rp
from coh.utils import find_subtrees, ilen

import numpy as np


class NounPhraseIncidence(base.Metric):
    """
        ## Incidência de Sintagmas:

        Incidência de sintagmas nominais por 1000 palavras.

        O desempenho da métrica é diretamente relacionada as árvores sintáticas
        de constituintes geradas pelo LX-Parser.

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        Como o texto possui 5 sintagmas nominais e 17 palavras a incidência
            de sintagmas é 294,11 (número de sintagmas/(número de palavras/1000
            )).
    """

    name = 'Noun Phrase Incidence'
    column_name = 'np_incidence'

    def value_for_text(self, t, rp=default_rp):
        parse_trees = rp.parse_trees(t)
        tagged_sents = rp.tagged_sentences(t)

        sent_indices = []
        for i, tree in enumerate(parse_trees):
            nps = len(find_subtrees(tree, 'NP'))
            words = len([word for word in tagged_sents[i]
                         if not rp.pos_tagger().tagset.is_punctuation(word)])

            sent_indices.append(nps / (words / 1000))

        return sum(sent_indices) / len(sent_indices) if sent_indices else 0


class MeanNounPhrase(base.Metric):
    """
    ## Média dos tamanhos médios dos sintagmas nominais nas sentenças
    """
    name = 'Mean Noun Phrase'
    column_name = 'mean_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        all_leaves = rp.leaves_in_toplevel_nps(t)
        mean_sizes = [np.mean([len(toplevel) for toplevel in sent]) for sent in all_leaves]
        return np.mean(mean_sizes)


class MaxNounPhrase(base.Metric):
    """
    ## Máximo dos tamanhos dos sintagmas nominais no texto
    """
    name = 'Maximum Noun Phrase'
    column_name = 'max_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        np_sizes = [len(toplevel)
                    for leaves in rp.leaves_in_toplevel_nps(t)
                    for toplevel in leaves]
        return max(np_sizes)


class MinNounPhrase(base.Metric):
    """
    ## Mínimo dos tamanhos dos sintagmas nominais no texto
    """
    name = 'Minimum Noun Phrase'
    column_name = 'min_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        np_sizes = [len(toplevel)
                    for leaves in rp.leaves_in_toplevel_nps(t)
                    for toplevel in leaves]
        return min(np_sizes)


class StdNounPhrase(base.Metric):
    """
    ## Desvio padrão dos tamanhos dos sintagmas nominais no texto
    """
    name = 'Std Noun Phrase'
    column_name = 'std_noun_phrase'

    def value_for_text(self, t, rp=default_rp):
        np_sizes = [len(toplevel)
                    for leaves in rp.leaves_in_toplevel_nps(t)
                    for toplevel in leaves]
        return np.std(np_sizes)


class WordsBeforeMainVerb(base.Metric):
    """
        ## Palavras Antes de Verbos Principais:

        Média de palavras antes de verbos principais na cláusula principal da
        sentença. Segundo a documentação do Coh-Metrix é um bom índice para
        avaliar a carga da memória de trabalho.

        O desempenho da métrica é diretamente relacionada as árvores sintáticas
        de dependência geradas pelo MaltParser e ao POS tagger do nlpnet.

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        Como este texto possui uma sentença o valor desta métrica
            corresponde ao valor de palavras antes do verbo desta única
            sentença que, neste caso, é 1 (a palavra acessório é a única que
            antecede o verbo).
    """

    name = 'Words before Main Verb'
    column_name = 'words_before_main_verb'

    def value_for_text(self, t, rp=default_rp):
        trees = rp.dep_trees(t)
        words = rp.tagged_words_in_sents(t)

        dep_tagset = rp.dep_parser().tagger.tagset
        tagset = rp.pos_tagger().tagset

        sent_scores = []
        for tree, tagged_sent in zip(trees, words):
            i_main_verb = 0

            i_root = [node['rel']
                      for node in tree.nodes.values()].index('ROOT')

            if dep_tagset.is_verb(
                    ('', list(tree.nodes.values())[i_root]['tag'])):
                # If the root of the dep. tree is a verb, use it.
                i_main_verb = i_root - 1
            else:
                # Otherwise, use the first verb that is not in the gerund,
                #   in the participle, or in the infinitive.
                for i, token in enumerate(tagged_sent):
                    if tagset.is_verb(token) \
                            and token[0][-2:] not in ('do', 'ar', 'er', 'ir'):
                        i_main_verb = i
                        break

            sent_scores.append(i_main_verb)

        return sum(sent_scores) / len(sent_scores) if sent_scores else 0


class Constituents(base.Category):
    """"""

    name = 'Constituents'
    table_name = 'constituents'

    def __init__(self):
        super(Constituents, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
