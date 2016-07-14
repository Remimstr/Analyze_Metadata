# Testing Spellcheck

<br />
## Workflow
<br />

##### 1) Build an Index file from a Standardized list file (for use in step 3)
**Use:** BuildSearchIndex.py from the SpellCheck directory <br  />
**Run as:** python BuildSearchIndex.py word_size inFile_path outFile_path indexFile_path <br />
**ex:** python BuildSearchIndex.py 3 Standard_Countries.txt Standard_Countries_out.txt Standard_Countries_index.txt
<br /><br />

##### 2) Make a list of "messed up" queries
**Use:** /scripts/make_spellcheck_mistakes.py <br />
**Run as:** python make_spellcheck_mistakes.py inFile_path outFile_path <br />
**ex:** python make_spellcheck_mistakes.py Standard_Countries.txt Messed_Countries.txt
<br /><br />

##### 3) Spellcheck the "messed up" queries using the Spellcheck module
**Use:** /scripts/evaluate_spellcheck.py <br />
**Run:** using one of the default setup options (Serovar, Provinces, Countries) <br />
&nbsp;&nbsp;&nbsp;&nbsp;**OR** <br />
**Run as:** python evaluate_spellcheck.py messedFile_path standardFile_path indexFile_path outFile_name <br />
**ex:** python evaluate_spellcheck.py Provinces
<br /><br />

##### 4) (Optional Step) Run eval_shortcut.awk to make assessment of the Spellcheck module easier
**Run as:** awk -f eval_shortcut.awk inFile_path.csv > outFile_path.csv

<br />
## Performance
<br />

Provinces, Countries, and Serovars were tested using this method, the results of which can be found in the results folder:
(SpellCheck_ProvincesValidation.xlsx, SpellCheck_CountriesValidation.xlsx, and SpellCheck_SeroValidation.xlsx). <br /><br />

Out of the countries that were messed up, 199/253 (78%) were correctly spellchecked, 43/253 (17%) were incorrectly 
spellchecked due to a mismatched first character, 11/253 (4.3%) were incorrectly spellchecked due to having no kmers
in common with the original query. 3/54 (5.5%) of incorrectly spellchecked strings resulted in incorrect guesses 
(false positives). <br /><br />

Out of the provinces that were messed up, 2055/2631 (78%) were correctly spellchecked, 405/2631 (15%) were incorrectly 
spellchecked due to a mismatched first character, 147/2631 (5.6%) were incorrectly spellchecked due to having no kmers
in common with the original query. The remaining queries (24/2632) (0.9%) were incorrectly spellchecked for various
valid reasons. 237/576 (41%) of incorrectly spellchecked strings resulted in incorrect guesses (false positives) <br /><br />

