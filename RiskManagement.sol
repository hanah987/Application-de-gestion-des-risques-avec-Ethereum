// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RiskManagement {
    // Struct pour représenter une contrepartie
    struct Counterparty {
        string name;
        uint256 exposureLimit; // Limite d'exposition en unité
        uint256 currentExposure; // Exposition actuelle
        bool exists; // Permet de vérifier si la contrepartie existe
    }

    // Mapping des contreparties
    mapping(address => Counterparty) private counterparties;

    // Événements
    event CounterpartyAdded(address indexed counterparty, string name, uint256 exposureLimit);
    event ExposureUpdated(address indexed counterparty, uint256 newExposure);
    event LimitExceeded(address indexed counterparty, uint256 currentExposure, uint256 exposureLimit);

    // Ajouter une nouvelle contrepartie
    function addCounterparty(address counterpartyAddress, string memory name, uint256 exposureLimit) public {
        require(!counterparties[counterpartyAddress].exists, "Contrepartie existe deja.");
        require(exposureLimit > 0, "La limite d'exposition doit etre superieure a zero.");

        counterparties[counterpartyAddress] = Counterparty({
            name: name,
            exposureLimit: exposureLimit,
            currentExposure: 0,
            exists: true
        });

        emit CounterpartyAdded(counterpartyAddress, name, exposureLimit);
    }

    // Mettre à jour l'exposition actuelle pour une contrepartie
    function updateExposure(address counterpartyAddress, uint256 newExposure) public {
        require(counterparties[counterpartyAddress].exists, "Contrepartie non trouvee.");

        Counterparty storage counterparty = counterparties[counterpartyAddress];
        counterparty.currentExposure = newExposure;

        emit ExposureUpdated(counterpartyAddress, newExposure);

        // Vérifier si la limite est dépassée
        if (newExposure > counterparty.exposureLimit) {
            emit LimitExceeded(counterpartyAddress, newExposure, counterparty.exposureLimit);
        }
    }

    // Calculer le ratio de risque (exposition actuelle / limite d'exposition)
    function calculateRisk(address counterpartyAddress) public view returns (uint256 riskRatio) {
        require(counterparties[counterpartyAddress].exists, "Contrepartie non trouvee.");

        Counterparty memory counterparty = counterparties[counterpartyAddress];
        require(counterparty.exposureLimit > 0, "Limite d'exposition non valide.");

        return (counterparty.currentExposure * 100) / counterparty.exposureLimit;
    }

    // Obtenir les détails d'une contrepartie
    function getCounterparty(address counterpartyAddress)
        public
        view
        returns (string memory name, uint256 exposureLimit, uint256 currentExposure)
    {
        require(counterparties[counterpartyAddress].exists, "Contrepartie non trouvee.");

        Counterparty memory counterparty = counterparties[counterpartyAddress];
        return (counterparty.name, counterparty.exposureLimit, counterparty.currentExposure);
    }
}
