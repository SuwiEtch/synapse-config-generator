/*
Copyright 2019 The Matrix.org Foundation C.I.C.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

import {
    SET_SERVERNAME,
    SET_STATS,
    SET_SECRET_KEY,
    GETTING_SECRET_KEY,
    SET_DELEGATION,
    SET_DELEGATION_PORTS,
    SET_DELEGATION_SERVERNAME,
    SET_REVERSE_PROXY,
    SET_TLS,
    TESTING_TLS_CERT_PATHS,
    SET_TLS_CERT_PATHS,
    SET_TLS_CERT_PATHS_VALIDITY,
    SET_TLS_CERT_FILES,
    UPLOADING_TLS_CERT_PATHS,
    TESTING_SYNAPSE_PORTS,
    SET_SYNAPSE_PORTS,
    SET_SYNAPSE_PORTS_FREE,
    SET_DATABASE,
    SET_CONFIG_DIR,
    BASE_CONFIG_CHECKED,
    SYNAPSE_START_FAILED,
    CONFIG_WRITE_FAILED,
} from "../actions/types";

export default (state, action) => {

    switch (action.type) {

        case BASE_CONFIG_CHECKED:
            return {
                ...state,
                baseConfigChecked: true,
                setupDone: action.setupDone,
            }
        case SET_SERVERNAME:
            return {
                ...state,
                servername: action.servername,
            }
        case SET_STATS:
            return {
                ...state,
                reportStats: action.consent,
            }
        case GETTING_SECRET_KEY:
            return {
                ...state,
                secretKeyLoaded: false,
            }
        case SET_SECRET_KEY:
            return {
                ...state,
                secretKeyLoaded: true,
                secretKey: action.key,
            };
        case SET_DELEGATION:
            return {
                ...state,
                delegationType: action.delegationType,
            }
        case SET_DELEGATION_PORTS:
            return {
                ...state,
                delegationFederationPort: action.federationPort,
                delegationClientPort: action.clientPort,
            }
        case SET_DELEGATION_SERVERNAME:
            return {
                ...state,
                delegationServername: action.servername,
            }
        case SET_REVERSE_PROXY:
            return {
                ...state,
                reverseProxy: action.proxyType,
            }
        case SET_TLS:
            return {
                ...state,
                tls: action.tlsType,
            }
        case TESTING_TLS_CERT_PATHS:
            return {
                ...state,
                testingCertPaths: action.testing,
            }
        case SET_TLS_CERT_PATHS_VALIDITY:
            return {
                ...state,
                certPathInvalid: action.certPathInvalid,
                certKeyPathInvalid: action.certKeyPathInvalid,
            }
        case SET_TLS_CERT_PATHS:
            return {
                ...state,
                tlsCertPath: action.certPath,
                tlsCertKeyPath: action.certKeyPath,
            }
        case SET_TLS_CERT_FILES:
            return {
                ...state,
                tlsCertFile: action.tlsCertFile,
                tlsCertKeyFile: action.tlsCerKeyFile,
            }
        case UPLOADING_TLS_CERT_PATHS:
            return {
                ...state,
                uploadingCerts: action.uploading,
            }
        case TESTING_SYNAPSE_PORTS:
            return {
                ...state,
                verifyingports: action.verifying,
            }
        case SET_SYNAPSE_PORTS:
            return {
                ...state,
                synapseFederationPort: action.federationPort,
                synapseClientPort: action.clientPort,
            }
        case SET_SYNAPSE_PORTS_FREE:
            return {
                ...state,
                synapseFederationPortFree: action.synapseFederationPortFree,
                synapseClientPortFree: action.synapseClientPortFree,
            }
        case SET_DATABASE:
            return {
                ...state,
                ...action.databaseConfig,
            }
        case SET_CONFIG_DIR:
            return {
                ...state,
                configDir: action.configDir,
            }
        case SYNAPSE_START_FAILED:
            return {
                ...state,
                synapseStartFailed: true,
            }
        default:
            return state;
        case CONFIG_WRITE_FAILED:
            return {
                ...state,
                configWriteFailed: true,
            }
    }

};
