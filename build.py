#!/usr/bin/env python3
"""Write the hermitpy notes site."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent

NAV = [
    ("index.html", "Overview"),
    ("use.html", "Use"),
    ("fragment.html", "Fragment"),
    ("classification.html", "Classification"),
    ("tableau.html", "Tableau"),
    ("errors.html", "Errors"),
]

FOOTER = (
    "hermitpy. A HermiT-style OWL reasoner in Python, without a JVM. "
    'Code: <a href="https://github.com/lamng3/hermitpy">github.com/lamng3/hermitpy</a>.'
)

REPO = "https://github.com/lamng3/hermitpy/blob/main/src/hermitpy"


def nav_html(current):
    links = ['<a class="brand-desk" href="index.html">hermitpy</a>']
    for href, label in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{current_attr}>{label}</a>')
    return "".join(links)


def page(filename, title, description, kicker, lede, body):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - hermitpy</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top">
  <a class="brand" href="index.html">hermitpy</a>
  <label class="nav-button" for="nav-toggle">Menu</label>
</header>
<input id="nav-toggle" class="nav-toggle" type="checkbox">
<div class="layout">
<nav class="nav">
{nav_html(filename)}
</nav>
<main id="content">
<p class="kicker">{kicker}</p>
<h1>{title}</h1>
<p class="lede">{lede}</p>
{body}
</main>
</div>
<footer class="site">{FOOTER}</footer>
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")


def main():
    page(
        "index.html",
        "Overview",
        "hermitpy is a HermiT-style OWL reasoner in Python. It checks consistency and builds a direct class hierarchy without a JVM.",
        "hermitpy",
        "A HermiT-style OWL reasoner in Python. It checks whether an ontology is consistent and builds a direct class hierarchy. Reasoning uses a hypertableau and does not need a JVM.",
        f"""
<nav class="toc"><strong>On this page</strong><ol><li><a href="#the-pieces">The pieces</a></li><li><a href="#one-call">One call</a></li><li><a href="#install">Install</a></li></ol></nav>
<p>The public entry is <code>Reasoner</code>. It reads an <code>rdflib</code> graph, rejects OWL outside a documented fragment, and answers consistency, unsatisfiable classes, and direct subclasses. The calculus follows Motik, Shearer, and Horrocks, &ldquo;Hypertableau Reasoning for Description Logics,&rdquo; Journal of Artificial Intelligence Research, 2009. hermitpy is LGPL-3.0-or-later. HermiT, the reasoner that introduced this calculus, is copyright Oxford University Computing Laboratory 2008&ndash;2014.</p>
<h2 id="the-pieces">The pieces</h2>
<div class="cards">
<a class="card" href="use.html"><strong>Use</strong><span><code>Reasoner</code>, consistency, unsatisfiable classes, and the direct hierarchy.</span></a>
<a class="card" href="fragment.html"><strong>Fragment</strong><span>The OWL constructs the loader accepts, and the ones it refuses.</span></a>
<a class="card" href="classification.html"><strong>Classification</strong><span>How subclass pairs, equivalents, and <code>owl:Nothing</code> are chosen.</span></a>
<a class="card" href="tableau.html"><strong>Tableau</strong><span>The completion graph: rules, blocking, clashes, and the search bounds.</span></a>
<a class="card" href="errors.html"><strong>Errors</strong><span><code>UnsupportedConstruct</code>, <code>InconsistentOntology</code>, and <code>ReasonerLimitExceeded</code>.</span></a>
</div>
<h2 id="one-call">One call</h2>
<pre><code>from rdflib import Graph
from hermitpy import Reasoner

graph = Graph()
graph.parse("ontology.ttl")
reasoner = Reasoner(graph)
reasoner.is_consistent()
reasoner.direct_subclasses()</code></pre>
<p><code>direct_subclasses</code> returns pairs of IRIs. Equivalent classes appear in both directions. Every satisfiable class with no stricter named parent is linked to <code>owl:Thing</code>. An inconsistent ontology raises <code>InconsistentOntology</code> instead of classifying every class as <code>owl:Nothing</code>.</p>
<h2 id="install">Install</h2>
<pre><code>git clone https://github.com/lamng3/hermitpy.git
cd hermitpy
pip install -e .</code></pre>
<p>Python 3.8 or newer. The only dependency is <code>rdflib</code>. Short scripts live in <code>examples/</code>. Tests are <code>python -m unittest discover</code>.</p>
""",
    )
    page(
        "use.html",
        "Use",
        "The hermitpy Reasoner: consistency, unsatisfiable classes, and a direct class hierarchy.",
        "hermitpy.Reasoner",
        "Construct a Reasoner from an rdflib graph that is already parsed. Turtle, RDF/XML, and the other formats rdflib accepts all work, because the loader sees the graph, not the file.",
        f"""
<nav class="toc"><strong>On this page</strong><ol><li><a href="#construct">Construct</a></li><li><a href="#methods">Methods</a></li><li><a href="#hierarchy">A small hierarchy</a></li><li><a href="#inconsistent">An inconsistent ontology</a></li></ol></nav>
<h2 id="construct">Construct</h2>
<pre><code>Reasoner(graph: Graph)</code></pre>
<p>Construction loads the graph. A construct outside the <a href="fragment.html">fragment</a> raises <code>UnsupportedConstruct</code> here, before any query. Source: <a href="{REPO}/reasoner.py">reasoner.py</a>.</p>
<h2 id="methods">Methods</h2>
<table>
<tr><th>Method</th><th>Returns</th><th>When it fails</th></tr>
<tr><td><code>is_consistent()</code></td><td><code>bool</code></td><td>Never, for a graph that loaded. The answer is cached on the reasoner.</td></tr>
<tr><td><code>unsatisfiable_classes()</code></td><td><code>list[str]</code></td><td>Named class IRIs that are empty in every model, sorted. If the ontology itself is inconsistent, every named class is returned.</td></tr>
<tr><td><code>direct_subclasses()</code></td><td><code>list[tuple[str, str]]</code></td><td>Direct <code>(subclass, superclass)</code> IRI pairs, sorted. Raises <code>InconsistentOntology</code> when the ontology has no model.</td></tr>
</table>
<p>IRIs are full strings, including <code>http://www.w3.org/2002/07/owl#Thing</code> and <code>http://www.w3.org/2002/07/owl#Nothing</code>. How those pairs are chosen is on the <a href="classification.html">Classification</a> page.</p>
<h2 id="hierarchy">A small hierarchy</h2>
<pre><code>from rdflib import Graph
from hermitpy import Reasoner

graph = Graph()
graph.parse(data='''
@prefix ex: &lt;https://example.org/&gt; .
ex:Dog rdfs:subClassOf ex:Animal .
ex:Animal rdfs:subClassOf ex:Organism .
''', format="turtle")

reasoner = Reasoner(graph)
print(reasoner.is_consistent())
for child, parent in reasoner.direct_subclasses():
    print(child, "subClassOf", parent)</code></pre>
<p>The pairs are <code>Animal</code> under <code>Organism</code>, <code>Dog</code> under <code>Animal</code>, and <code>Organism</code> under <code>owl:Thing</code>. <code>Dog</code> is not listed directly under <code>Organism</code> or <code>owl:Thing</code>. The same shape is <code>examples/hierarchy.py</code>.</p>
<h2 id="inconsistent">An inconsistent ontology</h2>
<pre><code>from hermitpy import InconsistentOntology

if reasoner.is_consistent():
    pairs = reasoner.direct_subclasses()
else:
    empty = reasoner.unsatisfiable_classes()</code></pre>
<p>Calling <code>direct_subclasses</code> on an ontology with no model raises <code>InconsistentOntology</code>. <code>examples/inconsistent.py</code> parses a file and prints <code>is_consistent()</code>.</p>
""",
    )
    page(
        "fragment.html",
        "Fragment",
        "The OWL fragment hermitpy accepts, and the constructs that raise UnsupportedConstruct.",
        "hermitpy.load",
        "The loader turns an rdflib graph into a TBox and an ABox. A construct outside the fragment raises UnsupportedConstruct. It is not dropped.",
        f"""
<nav class="toc"><strong>On this page</strong><ol><li><a href="#accepted">Accepted</a></li><li><a href="#datatypes">Datatypes</a></li><li><a href="#refused">Refused</a></li><li><a href="#ignored">Ignored</a></li><li><a href="#how-axioms-land">How axioms land</a></li></ol></nav>
<h2 id="accepted">Accepted</h2>
<table>
<tr><th>Construct</th><th>What the loader does</th></tr>
<tr><td>Named classes, <code>owl:Thing</code>, <code>owl:Nothing</code></td><td>Named IRIs other than Thing and Nothing are recorded as classes to classify.</td></tr>
<tr><td><code>rdfs:subClassOf</code></td><td>A named class on the left unfolds into its superclass. A complex left-hand side becomes a general inclusion.</td></tr>
<tr><td><code>owl:equivalentClass</code></td><td>Two inclusions, one each way. Equivalence of two properties is refused.</td></tr>
<tr><td><code>owl:disjointWith</code></td><td>Each class is a subclass of the complement of the other. Disjoint properties are refused.</td></tr>
<tr><td><code>owl:complementOf</code>, <code>owl:intersectionOf</code>, <code>owl:unionOf</code></td><td>Parsed and pushed into negation normal form.</td></tr>
<tr><td><code>owl:someValuesFrom</code>, <code>owl:allValuesFrom</code></td><td>Existential and universal restrictions on object properties, including inverse roles written with <code>owl:inverseOf</code>.</td></tr>
<tr><td><code>owl:inverseOf</code></td><td>Named inverses are recorded both ways. A property declared inverse of itself is treated as symmetric.</td></tr>
<tr><td><code>owl:TransitiveProperty</code>, <code>owl:SymmetricProperty</code></td><td>Named properties only. Transitivity is copied onto a named inverse.</td></tr>
<tr><td><code>rdfs:domain</code>, <code>rdfs:range</code></td><td>Object-property domain and range, applied to a role and to its inverse. A datatype-property domain is an existential over <code>rdfs:Literal</code>.</td></tr>
<tr><td>Class assertions</td><td><code>individual a Class</code> on a named individual.</td></tr>
<tr><td>Object-property assertions</td><td>Two named individuals and a named property.</td></tr>
<tr><td>Literal assertions</td><td>A named individual, a property, and a supported literal.</td></tr>
</table>
<p>Source: <a href="{REPO}/load.py">load.py</a>.</p>
<h2 id="datatypes">Datatypes</h2>
<p>Restrictions may use <code>owl:onDatatype</code> and <code>owl:withRestrictions</code> on a datatype property in the forward direction. The facets are <code>xsd:minInclusive</code>, <code>xsd:maxInclusive</code>, <code>xsd:minExclusive</code>, and <code>xsd:maxExclusive</code>. A datatype restriction on an inverse property is refused.</p>
<p>The numeric family is <code>xsd:integer</code>, <code>xsd:int</code>, <code>xsd:long</code>, <code>xsd:short</code>, <code>xsd:nonNegativeInteger</code>, <code>xsd:positiveInteger</code>, <code>xsd:nonPositiveInteger</code>, <code>xsd:negativeInteger</code>, <code>xsd:decimal</code>, <code>xsd:double</code>, <code>xsd:float</code>, <code>owl:real</code>, and <code>owl:rational</code>. Integer datatypes stay on integers when bounds are tightened. The other families are <code>xsd:string</code>, <code>xsd:anyURI</code>, <code>xsd:date</code>, <code>xsd:dateTime</code>, <code>xsd:boolean</code>, and <code>rdfs:Literal</code>. Any other datatype raises <code>UnsupportedConstruct</code>.</p>
<p>An existential numeric bound and a universal numeric bound that cannot overlap make the class unsatisfiable. The ontology can still be consistent.</p>
<h2 id="refused">Refused</h2>
<p>These raise <code>UnsupportedConstruct</code>. The exception names the construct. See <a href="errors.html">Errors</a>.</p>
<ul>
<li>Cardinality, including <code>owl:maxCardinality</code>, <code>owl:minCardinality</code>, <code>owl:qualifiedCardinality</code>, and the exact forms.</li>
<li>Property chains, role inclusion (<code>rdfs:subPropertyOf</code>), <code>owl:equivalentProperty</code>, and <code>owl:propertyDisjointWith</code>.</li>
<li>Nominals (<code>owl:oneOf</code>), keys, <code>owl:hasSelf</code>, and <code>owl:disjointUnionOf</code>.</li>
<li><code>owl:sameAs</code>, <code>owl:differentFrom</code>, <code>owl:AllDifferent</code>, <code>owl:AllDisjointClasses</code>, and <code>owl:AllDisjointProperties</code>.</li>
<li><code>owl:FunctionalProperty</code>, <code>owl:InverseFunctionalProperty</code>, <code>owl:AsymmetricProperty</code>, <code>owl:IrreflexiveProperty</code>, and <code>owl:ReflexiveProperty</code>.</li>
<li>Negative property assertions, SWRL, and <code>owl:imports</code>.</li>
<li>Anonymous individuals, anonymous transitive or symmetric properties, cyclic class expressions, and a property with two conflicting <code>owl:inverseOf</code> targets.</li>
</ul>
<p>Any OWL predicate outside the accepted set is refused the same way, so a new constructor is not silently skipped.</p>
<h2 id="ignored">Ignored</h2>
<p>Annotation triples are skipped: <code>rdfs:label</code>, <code>rdfs:comment</code>, <code>rdfs:seeAlso</code>, <code>rdfs:isDefinedBy</code>, <code>owl:versionInfo</code>, <code>owl:deprecated</code>, and any property typed <code>owl:AnnotationProperty</code>. Ontology header triples such as <code>owl:versionIRI</code>, <code>owl:priorVersion</code>, <code>owl:backwardCompatibleWith</code>, and <code>owl:incompatibleWith</code> are not axioms.</p>
<h2 id="how-axioms-land">How axioms land</h2>
<p>A subclass axiom whose left side is a named class is stored as an unfolding of that name. Unfolding is applied when the tableau sees the atom. A left side that is a conjunction, a restriction, or another complex concept is stored as a general concept inclusion and added to every node.</p>
<p><code>owl:Nothing</code> on the left of an inclusion is dropped. A superclass of <code>owl:Thing</code> is dropped. Declarations of <code>owl:Class</code>, <code>owl:ObjectProperty</code>, <code>owl:DatatypeProperty</code>, <code>owl:NamedIndividual</code>, and <code>owl:Ontology</code> are not class assertions.</p>
""",
    )
    page(
        "classification.html",
        "Classification",
        "How hermitpy decides consistency, unsatisfiable classes, and direct subclass pairs.",
        "hermitpy.Reasoner",
        "Consistency is a search over the whole ontology. Class subsumption is a separate search that ignores the ABox. The direct hierarchy is built from those subsumption answers.",
        f"""
<nav class="toc"><strong>On this page</strong><ol><li><a href="#consistency">Consistency</a></li><li><a href="#empty-classes">Empty classes</a></li><li><a href="#pairs">Direct pairs</a></li><li><a href="#equivalents">Equivalents</a></li><li><a href="#nothing">Unsatisfiable classes</a></li></ol></nav>
<h2 id="consistency">Consistency</h2>
<p><code>is_consistent</code> asks whether the loaded TBox and ABox together have a model. The first answer is cached. An empty graph is consistent and has no subclass pairs.</p>
<p>A class can be empty while the ontology stays consistent. <code>Unicorn</code> subclass of both <code>Horse</code> and <code>NotHorse</code>, with those two disjoint, is unsatisfiable, and the ontology still has a model: just do not use <code>Unicorn</code>.</p>
<h2 id="empty-classes">Empty classes</h2>
<p><code>unsatisfiable_classes</code> returns the sorted named classes for which the atom is not satisfiable in the TBox. That test ignores the ABox. The fragment has no nominals, so a consistent ABox does not change class subsumption.</p>
<p>If <code>is_consistent</code> is false, every named class is returned. There is no model in which to separate them.</p>
<h2 id="pairs">Direct pairs</h2>
<p><code>direct_subclasses</code> refuses an inconsistent ontology. It does not report every class as a subclass of <code>owl:Nothing</code>.</p>
<p>For a consistent ontology it tests subsumption between <code>owl:Thing</code> and each satisfiable named class. <code>A</code> is subsumed by <code>B</code> when <code>A</code> and not <code>B</code> is unsatisfiable in the TBox. A pair is direct when no third satisfiable class sits strictly between them. Every satisfiable class with no stricter named parent is paired with <code>owl:Thing</code>.</p>
<p>A chain <code>Dog</code> &sube; <code>Animal</code> &sube; <code>Organism</code> therefore yields three pairs: Dog&ndash;Animal, Animal&ndash;Organism, and Organism&ndash;Thing. Dog&ndash;Organism is omitted because Animal is between them.</p>
<h2 id="equivalents">Equivalents</h2>
<p>If two satisfiable named classes subsume each other, both directions are returned: <code>(Dog, Canine)</code> and <code>(Canine, Dog)</code>. Each of them is also linked to the same direct named parents. Neither is linked to <code>owl:Thing</code> when a stricter parent such as <code>Animal</code> exists.</p>
<h2 id="nothing">Unsatisfiable classes</h2>
<p>Each unsatisfiable named class is paired with <code>owl:Nothing</code>. Unsatisfiable classes are also reported as equivalent to each other, both directions. They are not placed under the satisfiable classes they were declared to subclass. Those declared parents are already implied by emptiness, and the hierarchy among satisfiable classes is computed separately.</p>
<p>Source: <a href="{REPO}/reasoner.py">reasoner.py</a>.</p>
""",
    )
    page(
        "tableau.html",
        "Tableau",
        "The hypertableau hermitpy uses: completion rules, blocking, datatype clashes, and the search bounds.",
        "hermitpy.tableau",
        "Satisfiability is a search over a completion graph. Nodes carry concepts in negation normal form. Edges are role successors. A clash closes a branch. An open, complete graph is a model.",
        f"""
<nav class="toc"><strong>On this page</strong><ol><li><a href="#two-questions">Two questions</a></li><li><a href="#rules">Rules</a></li><li><a href="#blocking">Blocking</a></li><li><a href="#data">Datatype clashes</a></li><li><a href="#bounds">Bounds</a></li></ol></nav>
<h2 id="two-questions">Two questions</h2>
<p>Ontology consistency starts from the ABox. Each named individual is a root node, class assertions and literal assertions label that node, and object-property assertions are edges.</p>
<p>Concept satisfiability starts from one fresh root labeled with the concept, plus the TBox. It does not copy the ABox. Callers check <code>is_consistent</code> first when they need the ontology, not a class, to have a model.</p>
<p>An empty ABox uses the same one-node start as a concept test with no extra concept, which asks whether the TBox alone is consistent.</p>
<h2 id="rules">Rules</h2>
<p>Each node is saturated before the search branches:</p>
<ol>
<li>Every general concept inclusion is added to the node.</li>
<li>A conjunction adds each operand.</li>
<li>A named class adds the concepts stored as its unfolding.</li>
<li>A universal restriction copies its filler to each neighbor along that role. On a transitive role, the universal itself is copied to the neighbor as well.</li>
<li>An edge adds the role's domain concepts to the source and its range concepts to the target.</li>
</ol>
<p><code>owl:Thing</code> is never stored. Adding a concept that is already on the node does nothing.</p>
<p>After saturation, an open disjunction is a choice point. The search tries each operand on a copy of the graph and stops at the first open branch. If every branch clashes, the concept is unsatisfiable.</p>
<p>Existential restrictions that are not yet witnessed create one successor and then saturate again. The successor is labeled with the filler, unless the filler is <code>owl:Thing</code>, in which case the edge alone is enough. Only one successor is created per pass.</p>
<h2 id="blocking">Blocking</h2>
<p>A node is blocked when an ancestor has the same label, that ancestor's parent has the same label as this node's parent, and both edges use the same role. A node under a blocked parent is blocked too. Blocked nodes do not spawn further successors. This pairwise check is what keeps inverses and transitive roles from building an infinite chain, as in a person who must have a person as a parent.</p>
<h2 id="data">Datatype clashes</h2>
<p>A node clashes when it contains <code>owl:Nothing</code>, or a named class and the negation of that same class. It also clashes when a datatype existential or an asserted literal cannot meet the universal restrictions on that property. Numeric bounds are intersected. A complemented range excludes its positive part. Distinct families, such as a number and a string, do not intersect, except that <code>rdfs:Literal</code> meets any family.</p>
<h2 id="bounds">Bounds</h2>
<p>The search refuses a graph of 256 nodes, and a branch deeper than 4096. Either case raises <code>ReasonerLimitExceeded</code>. Those bounds are safety stops for this fragment search. They are not a completeness proof for OWL beyond the <a href="fragment.html">fragment</a>.</p>
<p>Source: <a href="{REPO}/tableau.py">tableau.py</a> and <a href="{REPO}/syntax.py">syntax.py</a>.</p>
""",
    )
    page(
        "errors.html",
        "Errors",
        "The three exceptions hermitpy raises: unsupported OWL, an inconsistent ontology, and a search bound.",
        "hermitpy.errors",
        "Loading fails closed. Classification refuses an ontology with no model. The tableau stops if the graph or the branch grows past its bound.",
        f"""
<nav class="toc"><strong>On this page</strong><ol><li><a href="#unsupported">UnsupportedConstruct</a></li><li><a href="#inconsistent">InconsistentOntology</a></li><li><a href="#limit">ReasonerLimitExceeded</a></li></ol></nav>
<pre><code>from hermitpy import InconsistentOntology, ReasonerLimitExceeded, UnsupportedConstruct

try:
    pairs = reasoner.direct_subclasses()
except InconsistentOntology:
    print(reasoner.unsatisfiable_classes())
except UnsupportedConstruct as error:
    print(error.construct)
except ReasonerLimitExceeded:
    print("search bound")</code></pre>
<h2 id="unsupported">UnsupportedConstruct</h2>
<p>A <code>ValueError</code>. Raised while the graph is loaded, including from <code>Reasoner(...)</code>, when the ontology uses OWL outside the <a href="fragment.html">fragment</a>. The message is <code>Unsupported OWL construct: ...</code> and says the construct is not ignored.</p>
<p><code>error.construct</code> is the short name, such as <code>owl:maxCardinality</code>, <code>owl:oneOf</code>, <code>SWRL</code>, or <code>anonymous individual</code>. Source: <a href="{REPO}/errors.py">errors.py</a>.</p>
<h2 id="inconsistent">InconsistentOntology</h2>
<p>A <code>ValueError</code>. Raised only by <code>direct_subclasses</code> when <code>is_consistent</code> is false. <code>unsatisfiable_classes</code> does not raise it. On an inconsistent ontology that method returns every named class.</p>
<h2 id="limit">ReasonerLimitExceeded</h2>
<p>A <code>RuntimeError</code>. Raised when a completion graph reaches 256 nodes, or when nondeterministic search passes depth 4096. The node message says the fragment search did not terminate. The depth message says the tableau search depth was exceeded.</p>
""",
    )


if __name__ == "__main__":
    main()
