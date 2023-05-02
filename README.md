# UD_Spanish-COSER

UD_Spanish-COSER
This repository contains the datasets used to evaluate state-of-the-art POS taggers when dealing with spoken Spanish, as described in the paper by Bonilla et al. (2022). The datasets are in CoNLL-U format and were first produced automatically, and then corrected manually for UPOS and FEATS tags. HEAD, DEP, and DEPS were produced automatically. Additionally, a tutorial dataset was double-checked by experts.

The following is a list of the datasets included in this repository:

es_coser-ud-dev.conllu
es_coser-ud-test.conllu
es_coser-ud-train.conllu
es_coser-ud-tutorial.conllu

Additionally, the models_evaluation.py file in this repository includes code used in the evaluation of the POS taggers, as described in the paper.

To cite or check the results of using these datasets, please refer to the following paper:

Bonilla, J.E., Bouzouita, M., & Segundo Díaz, R.L. (2022). La construcción del Corpus Oral y Sonoro del Español Rural-Anotado y Parseado (COSER-AP): avances en el etiquetado de partes del discurso/The Construction of the Annotated and Parsed Audible Corpus of Spoken Rural Spanish (COSER-AP): Advances in the Annotation of the Parts of Speech. Revista Internacional de Lingüística Iberoamericana, 20(40), 77-96. https://www.degruyter.com/document/doi/10.31819/rili-2022-204006/html
