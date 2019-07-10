# COMP90042_Project_Automatic_Fact_Verification
This is the project of COMP90042 Web Search and Analysis. Group work by 2 master students.

---
### JSON Files Structure

```
"75397": {
	"claim": "Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.",
	"label": "SUPPORTS",
	"evidence": [
		["Fox_Broadcasting_Company", 0],
		["Nikolaj_Coster-Waldau", 7]
	]
}
```
<ul>
	<li><strong>claim</strong>: a fact that needs to verificate.</li>
	<li><strong>label</strong>: show the result of this claim.
		<ul>
			<li><code>SUPPORTS</code> : have evidence to support this claim.</li>
			<li><code>REFUTES</code> : have evidence to refute this claim.</li>
			<li><code>NOT ENOUGH INFO</code> : no evidence is provided for this claim.</li>
		</ul>
	</li>
	<li><strong>evidence</strong>: Show the evidence location</li>
		<ul>
			<li><code>"Fox_Broadcasting_Company"</code> : show the page identifier.</li>
			<li><code>0</code> : show the sentence index in that page.</li>
		</ul>
</ul>

---
### Verification Process

`>python score.py devset.json random-devset.json`

**deveset.json** is the actual result.<br/>
**random-devset.json** is the prediction result.<br/>
<br/>
In this project, we need edit the content of ``random-devset.json`` and increase the performance of the prediction system.<br/>

---
### Report Requirements
<ul>
	<li>the description, analysis, and comparative assessment (where applicable) of methods used</li>
	<li>Ymention any choices you made in implementing your system along with empirical justification for those choices</li>
	<li>error analysis of the basic system to motivate your enhancements and describe it encough details</li>
	<li>evaluate whether your enhancements increased performance as compared to the basic system</li>
	<li>also report your relative performance on the <strong>codalab leaderboard</strong></li>
	<li>(<strong>optional</strong>) discuss what steps you might take next if you were to continue development of your system</li>
</ul>


### Ongoing Improvement
<ul>
	<li>Learning-to-Ranking: after retrieval top-K documents, use machine learning method to determine how many documents are the relevant evidence for this claim. It is better than just use the BM25 to select document.</li>
	
</ul>
