package ExtractData;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Label;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.ling.Word;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreebankLanguagePack;
import edu.stanford.nlp.trees.TypedDependency;

public class Parser {

	private String grammar = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
	private String[] options = { "-maxLength", "80", "-retainTmpSubcategories" };
	private LexicalizedParser lp = LexicalizedParser
			.loadModel(grammar, options);
	private TreebankLanguagePack tlp = lp.getOp().langpack();
	private GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();

	public Parser() {
	}

	public LinkedList<String> getKeyWrodsFromSentence(String string) {
		LinkedList<String> list = new LinkedList<String>();

		String[] sent = string.split(" ");
		List<HasWord> sentence = new ArrayList<HasWord>();
		for (String word : sent)
			sentence.add(new Word(word));

		Tree parse = lp.parse(sentence);
		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);

		List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();

		String[] current;
		String type, key;
		List<CoreLabel> labelsList = parse.taggedLabeledYield();
		for (Label l : labelsList) {
			current = l.toString().split("-");
			type = current[0];
			if (type.equals("NN") || type.equals("NNS")) {
				key = sent[Integer.parseInt(current[1])];
				list.add(key);
			}
		}
		return list;
	}

	public LinkedList<String> getKeyWrodsFromSentenceTest(String string) {

		LinkedList<String> list = new LinkedList<String>();

		String[] sent = string.split(" ");
		List<HasWord> sentence = new ArrayList<HasWord>();
		for (String word : sent) {
			sentence.add(new Word(word));
		}

		Tree parse = lp.parse(sentence);
		parse.pennPrint();
		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);

		List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
		System.out.println(tdl);

		System.out.println();

		System.out.println("The words of the sentence:");
		for (Label lab : parse.yield()) {
			if (lab instanceof CoreLabel) {
				System.out.println(((CoreLabel) lab)
						.toString(CoreLabel.OutputFormat.VALUE_MAP));
			} else {
				System.out.println(lab);
			}
		}
		System.out.println();
		System.out.println("tagged");
		System.out.println(parse.taggedYield());

		List<CoreLabel> temp = parse.taggedLabeledYield();
		for (Label l : temp) {
			String[] sss = l.toString().split("-");
			String type = sss[0];
			System.out.println(sss[0] + "  " + sss[1] + "    "
					+ sent[Integer.parseInt(sss[1])]);
		}

		for (Iterator<String> ite = list.iterator(); ite.hasNext();)
			System.out.println(ite.next());
		return list;
	}

	public static void main(String[] args) throws IOException {
		Parser parser = new Parser();
		parser.getKeyWrodsFromSentence("When athletes begin to exercise, their heart rates and respiration rates increase.  At what level of organization does the human body coordinate these functions?");
		parser.getKeyWrodsFromSentenceTest("When athletes begin to exercise, their heart rates and respiration rates increase.  At what level of organization does the human body coordinate these functions?");
		// main2();

	}
}
