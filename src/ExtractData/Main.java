package ExtractData;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Iterator;
import java.util.LinkedList;

import com.csvreader.CsvReader;
import com.csvreader.CsvWriter;

public class Main {

	public static void PutKeyWordsIntoKeyWordsList(LinkedList<String> keyWords,
			DataStructure ds) {
		String str;
		for (Iterator<String> ite = keyWords.iterator(); ite.hasNext();) {
			str = ite.next();
			if (ds.contains(str)) {
			} else {
				ds.add(str);
			}
		}
	}

	public static void PutKeyWordsIntoKeyWordsList(LinkedList<String> keyWords,
			Dictionary ds, LinkedList<String> keyWordsList) {
		String str;
		for (Iterator<String> ite = keyWords.iterator(); ite.hasNext();) {
			str = ite.next();
			if (ds.contains(str)) {
			} else {
				ds.add(str);
				keyWordsList.add(str);
			}
		}
	}

	public static void action(String sentence, DataStructure ds, Parser parser) {
		sentence = sentence.replace(',', ' ');
		sentence = sentence.replace('.', ' ');
		sentence = sentence.replace('?', ' ');
		sentence = sentence.replace('_', ' ');
		sentence = sentence.toLowerCase();
		LinkedList<String> keyWords = parser.getKeyWrodsFromSentence(sentence);
		PutKeyWordsIntoKeyWordsList(keyWords, ds);
	}

	public static void Print(LinkedList<String> list) {
		String temp;
		for (Iterator<String> ite = list.iterator(); ite.hasNext();)
			System.out.println(ite.next());
	}

	public static void main(String[] args) throws IOException {

		CsvReader reader = new CsvReader("training_set.tsv");
		reader.setDelimiter('\t');
		reader.readHeaders();

		DataStructure ds = new DataStructure();
		Parser parser = new Parser();

		String[] str;
		String sentence = null;
		int instanceNum = 0;
		int exceptNum = 0;
		while (reader.readRecord()) {
			str = reader.getValues();
			str[1] = str[1].toLowerCase();

			for (int choice = 3; choice < 7; choice++) {
				sentence = str[1];
				if (str[1].contains("when")) {
					sentence.replace("when", str[choice]);
				} else if (str[1].contains("why")) {
					sentence.replace("why", str[choice]);
				} else if (str[1].contains("which")) {
					sentence.replace("which", str[choice]);
				} else if (str[1].contains("what")) {
					sentence.replace("what", str[choice]);
				} else if (str[1].contains("where")) {
					sentence.replace("where", str[choice]);
				} else if (str[1].contains("__")) {
					sentence.replace("__", str[choice]);
				} else {
					sentence = sentence + str[choice];
					exceptNum++;
				}
				action(sentence, ds, parser);

				instanceNum++;
				if (instanceNum % 100 == 0) {
					System.out.println(instanceNum + "  " + ds.size() + "  "
							+ exceptNum);
				}
			}

		}

		System.out.println(ds.size());
		System.out.println(exceptNum);
		ds.write("data.txt");
	}
}
