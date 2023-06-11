console.log("Integrated");

        async function clearCache() {
            if ('caches' in window) {
                try {
                    const cache = await caches.open('your_cache_name');
                    const keys = await cache.keys();
                    keys.forEach(key => cache.delete(key));
                    console.log('Cache cleared.');
                } catch (error) {
                    console.error('Error clearing cache:', error);
                }
            } else {
                console.error('Cache API is not supported in this browser.');
            }
        }

        async function connectAndEnableMetaMask() {
            if (typeof window.ethereum !== 'undefined') {
                const web3 = new Web3(window.ethereum);

                try {
                    await window.ethereum.enable();
                    console.log('Connected to MetaMask');
                } catch (error) {
                    console.error('Access to MetaMask accounts denied by user:', error);
                }
            } else {
                console.error('MetaMask is not installed.');
            }
        }

        async function transact(amount,slug) {
            const contractABI = [
        {
            "constant": false,
            "inputs": [
                {
                    "name": "us",
                    "type": "string"
                }
            ],
            "name": "addUser",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": true,
            "inputs": [],
            "name": "getUser",
            "outputs": [
                {
                    "name": "",
                    "type": "string"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": false,
            "inputs": [
                {
                    "name": "ad",
                    "type": "string"
                }
            ],
            "name": "addProduct",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": true,
            "inputs": [],
            "name": "getProduct",
            "outputs": [
                {
                    "name": "",
                    "type": "string"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": false,
            "inputs": [
                {
                    "name": "bo",
                    "type": "string"
                }
            ],
            "name": "bookOrder",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": true,
            "inputs": [],
            "name": "getOrder",
            "outputs": [
                {
                    "name": "",
                    "type": "string"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "sender",
                    "type": "address"
                },
                {
                    "indexed": false,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256"
                }
            ],
            "name": "Received",
            "type": "event"
        },
        {
            "constant": false,
            "inputs": [
                {
                    "name": "amount",
                    "type": "uint256"
                }
            ],
            "name": "receiveMoney",
            "outputs": [],
            "payable": true,
            "stateMutability": "payable",
            "type": "function"
        }
    ];
            const contractAddress = "0xF597653688B174DeF777C473f4c762E60DAe29cd";
            const web3 = new Web3(window.ethereum);
            const contract = new web3.eth.Contract(contractABI, contractAddress);
            const amountToSend = web3.utils.toWei('12', 'ether'); // Example: 1 Ether
            const fromAddress = (await web3.eth.getAccounts())[0];
            try {
                const transaction = await contract.methods.receiveMoney(amountToSend).send({
                    from: fromAddress,
                    value: amountToSend
                });
                
                console.log('Transaction successful:', transaction);
                url = "http://127.0.0.1:8000"+ slug
                window.location.href = url;
            } catch (error) {
                console.error('Error occurred during transaction:', error);

            }
        }

        window.addEventListener('load', async () => {
            await connectAndEnableMetaMask();
        
            const button = document.getElementById('transactionButton');
            const ip = document.getElementById('prize');
            const slug = document.getElementById('slug').value;
            const buttonValue = ip.value;
            console.log(buttonValue,slug)
            button.addEventListener('click', () => transact(`${buttonValue}`,`${slug}`));
        });
        