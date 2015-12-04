package TurnDataIntoCSV;

import java.io.*;
import java.util.*;

import ExtractData.*;

import com.csvreader.*;

public class Main {

	public static void write(String sentence, String[][] matrix,
			TreeMap<String, Integer> map, int instanceNum) {

		sentence = sentence.replace(',', ' ');
		sentence = sentence.replace('.', ' ');
		sentence = sentence.replace('?', ' ');
		sentence = sentence.replace('_', ' ');
		sentence = sentence.toLowerCase();

		String str;
		Scanner scan = new Scanner(sentence);
		while (scan.hasNext()) {
			str = scan.next();
			if (map.containsKey(str)) {
				matrix[instanceNum][map.get(str)] = "1";
			}
		}
	}

	public static String[] getString(String str[], String add) {
		int l = str.length;
		String neo[] = new String[l + 1];
		str[0] = add;
		for (int i = 1; i <= l; i++)
			neo[i - 1] = str[i - 1];
		return neo;
	}

	public static void writeTrainingFeature(String fromTxtFile,
			String referenceTsvFile, String toCsvFile) throws IOException {
		int M = 10000, N = 3587;

		TreeMap<String, Integer> map = new TreeMap<String, Integer>();

		String matrix[][] = new String[M][N];
		for (int i = 0; i < M; i++)
			Arrays.fill(matrix[i], "0");

		Scanner scan = new Scanner(new File(fromTxtFile));
		String[] classLabel = new String[N];
		int featureNum = 0;
		while (scan.hasNext()) {
			String str = scan.next().trim();
			map.put(str, featureNum);
			classLabel[featureNum] = str;
			featureNum++;
		}

		CsvReader reader = new CsvReader(referenceTsvFile);
		reader.setDelimiter('\t');
		reader.readHeaders();

		String[] instanceStr;
		int instanceNum = 0;
		while (reader.readRecord()) {
			instanceStr = reader.getValues();

			for (int choice = 3; choice < 7; choice++) {
				write(instanceStr[1] + instanceStr[choice], matrix, map,
						instanceNum);
				instanceNum++;
			}
		}

		CsvWriter writer = new CsvWriter(toCsvFile);
		for (int i = 0; i < instanceNum; i++)
			writer.writeRecord(matrix[i]);
		writer.flush();
		writer.close();

		// writer = new CsvWriter("complete data.csv");
		// writer.writeRecord(getString(classLabel, " "));
		// for (int i = 0; i < instanceNum; i++)
		// writer.writeRecord(getString(matrix[i], i + 1 + ""));
		// writer.flush();
		// writer.close();

	}

	public static void writeTestFeature(String fromTxtFile,
			String referenceTsvFile, String toCsvFile) throws IOException {

		TreeMap<String, Integer> map = new TreeMap<String, Integer>();
		int N = 8132 * 4, M = 3587;

		String matrix[][] = new String[N][M];
		for (int i = 0; i < N; i++)
			Arrays.fill(matrix[i], "0");

		Scanner scan = new Scanner(new File(fromTxtFile));
		String[] classLabel = new String[M];
		int featureNum = 0;
		while (scan.hasNext()) {
			String str = scan.next().trim();
			map.put(str, featureNum);
			classLabel[featureNum] = str;
			featureNum++;
		}

		CsvReader reader = new CsvReader(referenceTsvFile);
		reader.setDelimiter('\t');
		reader.readHeaders();

		String[] instanceStr;
		int instanceNum = 0;
		while (reader.readRecord()) {
			instanceStr = reader.getValues();
			for (int choice = 2; choice < 6; choice++) {
				write(instanceStr[1] + instanceStr[choice], matrix, map,
						instanceNum);
				instanceNum++;
			}
		}

		CsvWriter writer = new CsvWriter(toCsvFile);
		for (int i = 0; i < instanceNum; i++)
			writer.writeRecord(matrix[i]);
		writer.flush();
		writer.close();

		// writer = new CsvWriter("complete data.csv");
		// writer.writeRecord(getString(classLabel, " "));
		// for (int i = 0; i < instanceNum; i++)
		// writer.writeRecord(getString(matrix[i], i + 1 + ""));
		// writer.flush();
		// writer.close();

	}

	public static void writeClassLabel(String referenceTsvFile, String toCsvFile)
			throws IOException {
		CsvWriter writer = new CsvWriter(toCsvFile);

		CsvReader reader = new CsvReader(referenceTsvFile);
		reader.setDelimiter('\t');
		reader.readHeaders();

		String[] s0 = { "0" };
		String[] s1 = { "1" };
		String[] instanceStr;
		while (reader.readRecord()) {
			instanceStr = reader.getValues();

			int choice = instanceStr[2].charAt(0) - 'A';
			for (int j = 0; j < 4; j++)
				if (j == choice)
					writer.writeRecord(s1);
				else
					writer.writeRecord(s0);
		}

		writer.flush();
		writer.close();
	}

	public static void main(String[] args) throws IOException {
		// writeTrainingFeature("data.txt", "training_set.tsv",
		// "training_features.csv");
		// writeClassLabel("training_set.tsv", "training_class_labels.csv");
		writeTestFeature("data.txt", "validation_set.tsv", "test_features.csv");
	}
}
