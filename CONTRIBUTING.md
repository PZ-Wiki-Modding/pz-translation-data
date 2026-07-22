# Contributing
To contribute to the dataset, follow these steps to set up your development environment:
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Linux/Mac: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

This will format the singular JSON files on each commit, which are used to allow for a single source of truth for all translation files. The smaller JSON files are easier to manage and work with during development.

## Contact
You can find the creator of this dataset (SimKDT) in the [PZ Modding Community](https://pzwiki.net/wiki/PZ_Modding_Community).
