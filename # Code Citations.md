# Code Citations

## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg]
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg]
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg]
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg]
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/imotov/dotfiles/blob/38d051285e1e9da9ca29133ff53ab89c25dea806/setup/leafminer.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/feisuzhu/dotfiles/blob/a52edd9f7b0e8d0e9998188b1d19d7520f5f718f/snippets/install-nvidia-container-toolkit

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: unknown
https://github.com/gunyarakun/blog.wktk.co.jp/blob/679fc67e229c43426f3d68dd64441424a76f002a/_posts/ja/2024-03-15-aws-g5g-aarch64-arm64-pytorch-torchaudio-cu121-cuda-ubuntu.md

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```


## License: MIT
https://github.com/AgenttiX/linux-scripts/blob/945d70f948e62fd91dcbd66f4375bdfcaed0e521/drivers/install_cuda.sh

```
Great timing with Azure credits! Here's a detailed, practical instruction set to get GPU VMs running in Azure and connect them to your application.

---

## **Phase 1: Azure VM Setup**

### **Step 1: Choose the Right VM Size**

For your use case (dots.ocr / PaddleOCR / vLLM), recommended Azure GPU VM sizes:

| VM Size | GPU | VRAM | Cost/hr | Best For |
|---------|-----|------|---------|----------|
| `NC4as_T4_v3` | Tesla T4 | 16GB | ~$0.50 | Testing, small models |
| `NC8as_T4_v3` | Tesla T4 | 16GB | ~$0.75 | Light production |
| `NC24ads_A100_v4` | A100 | 80GB | ~$3.50 | Heavy models |
| `NV6ads_A10_v5` | A10 | 24GB | ~$0.90 | **Recommended start** |

**Start with `NC4as_T4_v3`** for testing (cheapest, enough for 7B-13B models).

---

### **Step 2: Create the VM**

```powershell
# Install Azure CLI on Windows
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name empower-ocr-rg --location eastus

# Create VM (Ubuntu 22.04 + T4 GPU)
az vm create `
  --resource-group empower-ocr-rg `
  --name empower-ocr-vm `
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest `
  --size Standard_NC4as_T4_v3 `
  --admin-username azureuser `
  --ssh-key-values ~/.ssh/id_rsa.pub `
  --os-disk-size-gb 128 `
  --public-ip-sku Standard

# Open required ports
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 11434 --priority 1001
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 8000 --priority 1002
az vm open-port --resource-group empower-ocr-rg --name empower-ocr-vm --port 443 --priority 1003

# Get public IP
az vm show --resource-group empower-ocr-rg --name empower-ocr-vm -d --query publicIps -o tsv
```

---

## **Phase 2: VM Configuration (SSH into VM)**

```bash
# SSH into VM
ssh azureuser@<YOUR_VM_PUBLIC_IP>
```

### **Step 3: Install NVIDIA Drivers + CUDA**

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install NVIDIA driver
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# SSH back in - verify GPU
nvidia-smi
# Should show: Tesla T4, 16GB
```

### **Step 4: Install Docker + NVIDIA Container Toolkit**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
```

