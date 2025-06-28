# GitHub & Vercel Automation Tool 🚀

An automated deployment tool that streamlines the process of creating GitHub repositories and deploying projects to Vercel. This tool handles the entire workflow from repository creation to deployment, making it perfect for rapid development and testing.

## 🌟 Features

- Automated GitHub repository creation and code pushing
- Automated Vercel project deployment
- JSON-based configuration for project structure
- Asynchronous file operations for better performance
- Environment-based configuration management
- Secure token handling for GitHub and Vercel authentication

## 📋 Prerequisites

Before you begin, ensure you have the following:

- Python 3.7 or higher
- A GitHub account with [Personal Access Token (PAT)](https://github.com/settings/tokens)
- A Vercel account with [Access Token](https://vercel.com/account/tokens)
- Git installed on your system

## 🔧 Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd automation_github_vercel
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Create a `.env` file in the root directory with the following variables:

```env
GITHUB_PAT_TOKEN=your_github_pat_token
GITHUB_USERNAME=your_github_username
VERCEL_TOKEN=your_vercel_token
```

2. Ensure your tokens have the necessary permissions:
   - GitHub PAT needs: `repo`, `workflow`
   - Vercel token needs: full access

## 📝 Project Structure

```
automation_github_vercel/
├── config.py                 # Configuration management
├── main.py                  # Main entry point
├── requirements.txt         # Python dependencies
├── src/
│   ├── controllers/        # Core controllers
│   │   ├── github.py      # GitHub operations
│   │   ├── load_data.py   # Data loading utilities
│   │   └── vercel.py      # Vercel operations
│   ├── core/
│   │   └── automatic_deployment.py  # Main automation logic
│   ├── lib/               # Utility libraries
│   └── utils/             # Helper functions
```

## 🚀 Usage

1. Prepare your project configuration in a JSON file (see `sample.json` for reference):

```json
{
  "workspace_generated_files": {
    "file_path": {
      "code": "file_content"
    }
  },
  "initial_files": {
    "file_path": {
      "code": "file_content"
    }
  }
}
```

2. Run the automation script:

```python
from src.core.automatic_deployment import automatic_deployment

deployment_url, hosted_url, is_error = await automatic_deployment(
    json_file_path="path/to/your/config.json",
    uuid="unique_identifier",
    repo_name="your_repo_name"
)
```

3. The script will:
   - Create a new GitHub repository
   - Push the project files
   - Deploy to Vercel
   - Return the deployment URLs

## 🔍 Response Format

The `automatic_deployment` function returns a tuple containing:

- `deployment_url`: Vercel deployment URL
- `hosted_url`: Final hosted project URL
- `is_error`: Boolean indicating if any errors occurred

## 🛠️ Error Handling

The system includes comprehensive error handling for:

- Invalid tokens
- Repository creation failures
- Deployment issues
- File system operations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## ⚠️ Important Notes

- Keep your tokens secure and never commit them to version control
- Ensure your GitHub and Vercel accounts have the necessary permissions
- Monitor your API rate limits for both GitHub and Vercel
- Regular backups of your configuration are recommended

## 🔗 Additional Resources
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Vercel API Documentation](https://vercel.com/docs/api)
