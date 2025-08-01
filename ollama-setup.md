# 🦙 Ollama Local LLM Setup Guide

This guide walks you through setting up Ollama to run local Large Language Models (LLMs) on your machine.

## 📋 Prerequisites

- Linux, macOS, or Windows (with WSL2)
- At least 8GB of RAM (16GB+ recommended)
- Internet connection for initial setup

## 🚀 Quick Start

### Step 1: Install Ollama

Run the following command to install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Alternative Installation Methods:**
- **macOS**: `brew install ollama`
- **Windows**: Download from [ollama.com](https://ollama.com)

### Step 2: Start the Ollama Server

Launch the Ollama server:

```bash
ollama serve
```

The server will start and listen on `http://localhost:11434` by default.

> 💡 **Tip**: Keep this terminal window open while using Ollama, or run it in the background.

### Step 3: Add Your Model

#### 3.1 Create a Modelfile

First, create a Modelfile that points to your local model:

```bash
echo 'FROM <file_path>' > Modelfile
```

**Example:**
```bash
echo 'FROM ./tinyllama.gguf' > Modelfile
```

#### 3.2 Import the Model

Attach your model to the Ollama server:

```bash
ollama create tinyllama -f Modelfile
```

Replace `tinyllama` with your preferred model name.

### Step 4: Verify Your Setup

Check that your model was successfully added:

```bash
ollama list
```

You should see your model listed.

## 🧪 Testing Your Model

### Command Line Chat

Start an interactive chat session:

```bash
ollama run tinyllama
```

### API Testing

Test the API with curl:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "tinyllama",
  "prompt": "Hello, how are you?",
  "stream": false
}' -H "Content-Type: application/json"
```

### Python Integration

```python
from langchain_ollama import ChatOllama

chat = ChatOllama(model="tinyllama", base_url="http://localhost:11434")
response = chat.invoke("Hello, world!")
print(response.content)
```

## 📁 Supported Model Formats

- **GGUF** (recommended): `.gguf` files
- **GGML**: `.ggml` files  
- **Safetensors**: `.safetensors` files

## 🔧 Common Commands

| Command | Description |
|---------|-------------|
| `ollama list` | Show installed models |
| `ollama run <model>` | Start interactive chat |
| `ollama pull <model>` | Download model from registry |
| `ollama rm <model>` | Remove a model |
| `ollama show <model>` | Show model information |

## 🌐 Using with Applications

Once your model is running, you can connect to it from:

- **Web applications** via HTTP API (`localhost:11434`)
- **Python scripts** using `langchain_ollama` or `requests`
- **Desktop applications** that support Ollama
- **VS Code extensions** for AI assistance

## 🔍 Popular Models to Try

You can download pre-trained models directly:

```bash
# Download and run popular models
ollama pull llama2          # Meta's Llama 2
ollama pull codellama       # Code-focused model  
ollama pull mistral         # Mistral 7B
ollama pull phi             # Microsoft's Phi model
```

## 🛠️ Troubleshooting

### Model Not Found
```bash
# Check if model exists
ollama list

# Re-create model if needed
ollama create <model-name> -f Modelfile
```

### Server Not Responding
```bash
# Check if server is running
curl http://localhost:11434/api/tags

# Restart server if needed
ollama serve
```

### Port Already in Use
```bash
# Run on different port
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

## 📚 Additional Resources

- [Official Ollama Documentation](https://ollama.com/docs)
- [Model Library](https://ollama.com/library)
- [GitHub Repository](https://github.com/ollama/ollama)

## 🎉 You're Ready!

Your local LLM is now running and ready to use. You can integrate it into your applications, chat with it directly, or use it for development projects.

Happy coding! 🚀
