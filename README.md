# Overview

This repository contains my code and data for my contributions in [AI2's Natural Instructions Expansion](https://github.com/allenai/natural-instructions-expansion) repository.

I have contributed the following datasets:

* [Detoxifying Language Models Risks Marginalizing Minority Voices](https://aclanthology.org/2021.naacl-main.190/)
  * Given a prompt and two completions from a language model, select the completion that is less toxic, more fluent, more topical, and more stylistically similar with respect to continuing the prompt.
* [SCAN](https://arxiv.org/abs/1711.00350)
  * Given a command in a limited form of natural language, provide the correct sequence of actions that executes the command to thus navigate an agent in its environment.
* [Odd-Man-Out](https://aclanthology.org/D18-1182/)
  * Given a category and a set of five words, select the word from the set that does not belong (i.e. is the least relevant) with the other words in the category.
* [ToM QA](https://arxiv.org/abs/1808.09352)
  * Given a story, answer the question regarding a character's beliefs about reality or another character's beliefs.
* [CODAH](https://arxiv.org/abs/1904.04365)
  * Given a prompt and four completions, select the completion that is the most plausible in continuing or answering the prompt.

So far with these 5 datasets, I have contributed 18 tasks, totaling to 81,587 instances. Each task is a variation of the description in each indented bulletpoint above. See the `.json` files in each directory for more information on each task.
