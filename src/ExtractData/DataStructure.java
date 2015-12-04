package ExtractData;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Iterator;
import java.util.concurrent.locks.ReentrantReadWriteLock.WriteLock;

public class DataStructure {
	public HashSet<String> hashSet;

	public DataStructure() {
		hashSet = new HashSet<String>();
	}

	public boolean contains(String str) {
		return hashSet.contains(str);
	}

	public void add(String str) {
		hashSet.add(str);
	}

	public int size() {
		return hashSet.size();
	}

	public void write(String filename) throws FileNotFoundException {
		PrintWriter writer = new PrintWriter(new File(filename));
		for (Iterator<String> ite = hashSet.iterator(); ite.hasNext();) {
			writer.write(ite.next() + "\t");
		}
		writer.flush();
		writer.close();
	}

}
