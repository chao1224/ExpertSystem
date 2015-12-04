package ExtractData;
import java.io.*;
import java.util.*;

public class Dictionary {
	class Trie {
		class TrieNode {
			private String s;
			private HashMap<Character, TrieNode> child;
			private TrieNode parent;
			boolean isWord;

			public TrieNode(boolean isWord) {
				s = "";
				parent = null;
				child = new HashMap<Character, TrieNode>();
				this.isWord = isWord;
			}

			public String getString() {
				return s;
			}

			public void setString(String s) {
				this.s = s;
			}

			public TrieNode addChild(char c, boolean isEnd) {
				TrieNode node = new TrieNode(isEnd);
				node.setParent(this);
				node.setString(s + c);
				child.put(c, node);
				return node;
			}

			public TrieNode getChild(char c) {
				return child.get(c);
			}

			public void removeChild(char c) {
				child.remove(c);
			}

			public boolean hasChild(char c) {
				return child.containsKey(c);
			}

			// If the TrieNode has any child
			public boolean isEmpty() {
				return child.isEmpty();
			}

			public TrieNode getParent() {
				return parent;
			}

			public void setParent(TrieNode parent) {
				this.parent = parent;
			}

			public char getChar() {
				return s.charAt(s.length() - 1);
			}

			public String toString() {
				String s = "";
				if (isWord)
					s += getString() + "\n";
				for (char c : child.keySet()) {
					s += child.get(c);
				}
				return s;
			}

			TrieNode findWord() {
				Queue<TrieNode> queue = new LinkedList<TrieNode>();
				TrieNode node = this;
				queue.add(node);
				while (!queue.isEmpty()) {
					if (node.isWord)
						return node;
					for (char c : node.child.keySet()) {
						queue.add(node.getChild(c));
					}
					node = queue.poll();
				}
				return null;
			}

			public int numWords() {
				int num = 0;
				if (isWord)
					num += 1;
				for (char c : child.keySet()) {
					num += child.get(c).numWords();
				}
				return num;
			}

			public void write(BufferedOutputStream os) throws IOException {
				if (isWord)
					os.write((s + "\n").getBytes());
				for (char c : child.keySet()) {
					child.get(c).write(os);
				}
			}
		}

		private TrieNode root;

		public Trie(char c) {
			root = new TrieNode(false);
			root.setString(Character.toString(c));
		}

		public TrieNode tryFind(String s) {

			TrieNode node = root;
			int i = 1;
			for (; i < s.length(); i++) {
				if (!node.hasChild(s.charAt(i)))
					break;
				node = node.getChild(s.charAt(i));
			}
			if (!node.isWord)
				node = node.findWord();
			String ss = findComSubstr(node.getString(), s);
			if (ss.length() < s.length() - 3
					|| ss.length() < node.getString().length() - 3)
				return null;
			return node;
		}

		public void addWord(String s) {
			TrieNode node = root;
			for (int i = 1; i < s.length(); i++) {
				if (!node.hasChild(s.charAt(i)))
					node.addChild(s.charAt(i), false);
				node = node.getChild(s.charAt(i));
			}
			node.isWord = true;
		}

		private String findComSubstr(String a, String b) {
			int i = 0;
			for (; i < Math.min(a.length(), b.length()); i++) {
				if (a.charAt(i) != b.charAt(i))
					break;
			}
			return a.substring(0, i);
		}

		// Shrink from a to b (assuming b is substring of a)
		public void shrink(String a, String b) {
			TrieNode longNode = tryFind(a);
			b = findComSubstr(a, b);
			while (longNode.getString().length() != b.length()) {
				TrieNode temp = longNode;
				longNode = longNode.getParent();
				if (temp.isEmpty())
					longNode.removeChild(temp.getChar());
				else
					break;
			}
			longNode.isWord = true;
		}

		public boolean isRoot(TrieNode t) {
			return root == t;
		}

		public String toString() {
			return root.toString();
		}

		public int size() {

			return root.numWords();
		}

		public void write(BufferedOutputStream os) throws IOException {
			root.write(os);
		}
	}

	private HashMap<Character, Trie> trie;

	public Dictionary() {
		trie = new HashMap<Character, Trie>();
	}

	public boolean contains(String s) {
		if (s.isEmpty())
			return false;
		Trie t = trie.get(s.charAt(0));
		if (t == null) {
			return false;
		}
		Trie.TrieNode node = t.tryFind(s);
		if (node == null) {
			return false;
		}
		if (s.length() < node.getString().length())
			t.shrink(node.getString(), s);

		return true;
	}

	public void add(String s) {
		if (s.isEmpty())
			return;
		if (!contains(s)) {
			Trie t = trie.get(s.charAt(0));
			if (t == null) {
				t = new Trie(s.charAt(0));
				trie.put(s.charAt(0), t);
			}
			t.addWord(s);

		}
	}

	public String toString() {
		String str = "";
		for (char c : trie.keySet()) {
			str += trie.get(c);
		}
		return str;
	}

	public int size() {
		int sz = 0;
		for (char c : trie.keySet()) {
			sz += trie.get(c).size();
		}
		return sz;
	}

	public void write(String filename) throws IOException {
		try {
			BufferedOutputStream os = new BufferedOutputStream(
					new FileOutputStream(new File(filename)));
			for (char c : trie.keySet()) {
				trie.get(c).write(os);
			}
			os.close();
		} catch (FileNotFoundException e) {
			System.err.println("Error: " + filename + " is not found");
		}

	}
}
