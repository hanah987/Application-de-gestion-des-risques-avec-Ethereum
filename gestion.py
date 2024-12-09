import streamlit as st
from web3 import Web3
import json

# Configuration Web3
st.title("Application de gestion des risques avec Ethereum")

# Connexion au réseau Ethereum (testnet ou local Ganache)
web3 = Web3(Web3.HTTPProvider("https://polygon-amoy.infura.io/v3/939d6fdcad1c406192cd99a4ee76015c"))  # Replace with your node URL
if web3.is_connected():
    st.success("Connecté au réseau Ethereum")
else:
    st.error("Échec de la connexion au réseau Ethereum")

# Adresse du contrat déployé
contract_address = Web3.to_checksum_address("0x95d33426fc4c06615e4b17f71ad22fe9fea38e84")  # Remplacez par l'adresse de votre contrat

# ABI du contrat - définit les fonctions disponibles dans le smart contract	
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "counterparty",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "exposureLimit",
				"type": "uint256"
			}
		],
		"name": "CounterpartyAdded",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "counterparty",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "newExposure",
				"type": "uint256"
			}
		],
		"name": "ExposureUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "counterparty",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "currentExposure",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "exposureLimit",
				"type": "uint256"
			}
		],
		"name": "LimitExceeded",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "counterpartyAddress",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "exposureLimit",
				"type": "uint256"
			}
		],
		"name": "addCounterparty",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "counterpartyAddress",
				"type": "address"
			}
		],
		"name": "calculateRisk",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "riskRatio",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "counterpartyAddress",
				"type": "address"
			}
		],
		"name": "getCounterparty",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "exposureLimit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "currentExposure",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "counterpartyAddress",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "newExposure",
				"type": "uint256"
			}
		],
		"name": "updateExposure",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Fonctionnalités principales
st.sidebar.title("Menu")
menu = st.sidebar.selectbox(
    "Choisissez une action",
    ["Ajouter une contrepartie", "Mettre à jour une exposition", "Consulter les détails d'une contrepartie"]
)

account = st.sidebar.text_input("0x5C3519e11968F75fEC5Ff598b72fFc834A5491BC")
private_key = st.sidebar.text_input("59c22540786ca68d10eae8fc6f15e808be5a92e451d1db54d75e3ad00ef01c79", type="password")  # Utilisez avec précaution en prod

if menu == "Ajouter une contrepartie":
    st.header("Ajouter une nouvelle contrepartie")
    counterparty_address = st.text_input("Adresse Ethereum de la contrepartie")
    name = st.text_input("Nom de la contrepartie")
    exposure_limit = st.number_input("Limite d'exposition", min_value=1, step=1)

    if st.button("Ajouter la contrepartie"):
        try:
            tx = contract.functions.addCcounterparty(
                counterparty_address, name, exposure_limit
            ).build_transaction({
                "from": account,
                "gas": 3000000,
                "nonce": web3.eth.get_transactionCount(account)
            })

            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            st.success(f"Transaction envoyée avec succès : {web3.toHex(tx_hash)}")
        except Exception as e:
            st.error(f"Erreur : {e}")

elif menu == "Mettre à jour une exposition":
    st.header("Mettre à jour l'exposition d'une contrepartie")
    counterparty_address = st.text_input("Adresse Ethereum de la contrepartie")
    new_exposure = st.number_input("Nouvelle exposition", min_value=0, step=1)

    if st.button("Mettre à jour"):
        try:
            tx = contract.functions.update_exposure(
                counterparty_address, new_exposure
            ).buildTransaction({
                "from": account,
                "gas": 3000000,
                "nonce": web3.eth.get_transactionCount(account)
            })

            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            st.success(f"Transaction envoyée avec succès : {web3.to_hex(tx_hash)}")
        except Exception as e:
            st.error(f"Erreur : {e}")

elif menu == "Consulter les détails d'une contrepartie":
    st.header("Consulter les détails d'une contrepartie")
    counterparty_address = st.text_input("Adresse Ethereum de la contrepartie")

    if st.button("Obtenir les détails"):
        try:
            details = contract.functions.get_counterparty(counterparty_address).call()
            st.write("Nom :", details[0])
            st.write("Limite d'exposition :", details[1])
            st.write("Exposition actuelle :", details[2])
        except Exception as e:
            st.error(f"Erreur : {e}")
