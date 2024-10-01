# ML-Firewall: RandomForest Parameter Tuning for Firewall Automation

## Overview
**ML-Firewall** is a machine learning-powered project that automates firewall rule optimization. It utilizes a **RandomForest model** to identify the top 10 important parameters from the dataset, which are stored in `Forest_Tree_output.txt`. These parameters are then used in a firewall configuration, managed through a bash script (`firewall_automation.sh`), enabling efficient and dynamic firewall rules.

## Features
- **Machine Learning Integration**: Uses a RandomForest model to analyze and rank parameters based on importance.
- **Firewall Automation**: Automates firewall rule updates based on the top 10 parameters found by the model.
- **Bash Scripting**: A bash script manages the configuration of the firewall using the extracted parameters.
- **Parameter Storage**: Important parameters are saved in `Forest_Tree_output.txt` for future reference and automation.

## How to Use

### Enable Automation:
```bash
sudo ./scripts/firewall_automation.sh enable
```

### Disable Automation:
```bash
sudo ./scripts/firewall_automation.sh disable
```

### Check the Status:
```bash
sudo ./scripts/firewall_automation.sh status
```
## Contributing

Feel free to open issues or submit pull requests for any improvements. Contributions are welcome!
