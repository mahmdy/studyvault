# 📚 StudyVault

StudyVault is an interactive command-line Python application designed to help students and knowledge workers store, update, delete, and search structured notes in Markdown (`.md`) files.

It acts as a personal knowledge base, allowing you to create or load existing data libraries and interact with them efficiently using simple, readable commands.

---

## 🚀 Features

- 📁 **Create** and manage study libraries as Markdown files
- 📝 **Store** new entries with section titles
- ✏️ **Update** specific text within a library
- ❌ **Delete** text from selected lines
- ➕ **Append** content to the start, end, or near a line within a section
- 🔍 **Search** across the entire file or specific sections
- 📑 **Index** all top-level section headers and view their content
- 📄 **Export** the current library to a clean and readable PDF file
- 🎨 Beautiful console UI with colorized prompts (thanks to `rich`)
- 💡 Linux arrow key support with `gnureadline`

---

## ⚙️ Setup Instructions

Below are step-by-step setup instructions for both Linux and Windows environments using a Python virtual environment (`venv`)

---

### 🐧 Linux Setup

1. Install Python (if not already installed)

```
bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```
2. (Optional) Install readline support for better CLI editing
To enable arrow keys and command history inside the CLI:

```
sudo apt install libreadline-dev
```

3. Clone the Repository

```
git clone https://github.com/your-username/StudyVault.git
cd StudyVault
```

4. Create a Virtual Environment

```
python3 -m venv venv
```

5. Activate the Virtual Environment

```
source venv/bin/activate
```

6. Install StudyVault in Editable Mode

```
pip install -e .

```

### 🪟 Windows Setup

1. Install Python from python.org
Ensure to check the box: Add Python to PATH during installation.

2. Open Command Prompt or PowerShell
Navigate to the directory where you want to clone the project:

```
git clone https://github.com/your-username/StudyVault.git
cd StudyVault
```

3. Install StudyVault in Editable Mode

```
pip install -e .
```

### 🧪 Usage
Once installed, simply run:

```
studyvault
```

### 📁 Data Storage

All knowledge files are stored in Markdown format (.md) within the data_libraries/ directory. These files are:

Human-readable

Markdown-editable

Easy to organize and back up

### 🧠 Command Menu
## 📌 Main Menu
	Create - Create a new data library

	List - Load and choose from existing libraries

	Exit - Exit the program

## 📌 Library Menu (after loading a library)
	Index - View a list of all section headers

	Store - Add a new titled section

	Update - Update text (format: Update: "old" with: "new")

	Delete - Remove text by choosing specific lines

	Append - Add data to a section at start/end/line

	Search - Search for keywords across the whole file

	Export - Export the current library as PDF

	Exit - Exit the program

### 📤 Exporting to PDF
	StudyVault supports clean PDF exports using reportlab. PDFs are saved into an exports/ folder.

	You'll be prompted for an output filename — or accept the default.

### 📎 Notes
	Use double quotes ("like this") when running the Update: command

	All content is stored in the data_libraries/ folder as .md files

	Exported PDFs are stored in the exports/ folder


### 🧪 Development & Testing
If you'd like to contribute or test individual functions, you can run:
```
python -m studyvault.main
```

### 🛠 Requirements
```
rich
markdown2
reportlab
gnureadline  # Only needed on Linux
```

## 📝 License

This project is licensed under the terms of the [MIT License](LICENSE).

You are free to use, modify, and distribute this software, with proper attribution, under the conditions of the MIT license.



### 🤝 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss the proposal.

### ✨ Author
Built with ❤️ by Mahmoud Neana, with support from ChatGPT
🔗 GitHub: https://github.com/mahmdy/studyvault