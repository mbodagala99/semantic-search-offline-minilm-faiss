import json
import os
from typing import Dict, Any, Optional

class OpenSearchServerResolver:
    """
    Simple OpenSearch server resolver using unique server IDs.
    Dynamically generates index URLs from server configurations.
    """
    
    def __init__(self, 
                 servers_config_file: str = 'configurations/opensearch_servers.json',
                 index_mappings_file: str = 'configurations/opensearch_index_mappings.json'):
        """
        Initialize the OpenSearch server resolver.
        
        Args:
            servers_config_file: Path to OpenSearch servers configuration file
            index_mappings_file: Path to OpenSearch index mappings file
        """
        self.servers_config_file = servers_config_file
        self.index_mappings_file = index_mappings_file
        
        # Load configurations
        self.servers_config = self._load_servers_config()
        self.index_mappings = self._load_index_mappings()
    
    def _load_servers_config(self) -> Dict[str, Any]:
        """Load OpenSearch servers configuration."""
        try:
            with open(self.servers_config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Servers config file '{self.servers_config_file}' not found. Using defaults.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in servers config file '{self.servers_config_file}'. Using defaults.")
            return {}
    
    def _load_index_mappings(self) -> Dict[str, Any]:
        """Load OpenSearch index mappings configuration."""
        try:
            with open(self.index_mappings_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Index mappings file '{self.index_mappings_file}' not found. Using defaults.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in index mappings file '{self.index_mappings_file}'. Using defaults.")
            return {}
    
    def get_server_config(self, server_id: str) -> Dict[str, Any]:
        """
        Get server configuration by server ID.
        
        Args:
            server_id: Unique server identifier
            
        Returns:
            Server configuration dictionary
        """
        servers = self.servers_config.get('servers', {})
        return servers.get(server_id, {})
    
    def get_index_server_id(self, index_name: str) -> str:
        """
        Get server ID for a specific index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Server ID for the index
        """
        index_mappings = self.index_mappings.get('index_mappings', {})
        index_config = index_mappings.get(index_name, {})
        return index_config.get('server_id', '')
    
    def get_cluster_url(self, index_name: str) -> str:
        """
        Get OpenSearch cluster URL for the specified index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            OpenSearch cluster URL
        """
        server_id = self.get_index_server_id(index_name)
        if not server_id:
            return 'http://localhost:9200'
        
        server_config = self.get_server_config(server_id)
        return server_config.get('cluster_url', 'http://localhost:9200')
    
    def get_index_url(self, index_name: str) -> str:
        """
        Dynamically generate OpenSearch index URL.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Complete OpenSearch index URL
        """
        cluster_url = self.get_cluster_url(index_name)
        return f"{cluster_url.rstrip('/')}/{index_name}"
    
    def get_authentication_config(self, index_name: str) -> Dict[str, Any]:
        """
        Get authentication configuration for the index's server.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Authentication configuration dictionary
        """
        server_id = self.get_index_server_id(index_name)
        if not server_id:
            return {"type": "none", "username": "", "password": ""}
        
        server_config = self.get_server_config(server_id)
        return server_config.get('authentication', {
            "type": "none",
            "username": "",
            "password": ""
        })
    
    def get_connection_settings(self, index_name: str) -> Dict[str, Any]:
        """
        Get connection settings for the index's server.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Connection settings dictionary
        """
        server_id = self.get_index_server_id(index_name)
        if not server_id:
            return {"timeout": 30, "max_retries": 3, "verify_certs": True}
        
        server_config = self.get_server_config(server_id)
        return server_config.get('connection_settings', {
            "timeout": 30,
            "max_retries": 3,
            "verify_certs": True
        })
    
    def resolve_complete_config(self, index_name: str) -> Dict[str, Any]:
        """
        Resolve complete OpenSearch configuration for an index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Complete configuration dictionary
        """
        server_id = self.get_index_server_id(index_name)
        server_config = self.get_server_config(server_id)
        
        return {
            "index_name": index_name,
            "server_id": server_id,
            "cluster_url": self.get_cluster_url(index_name),
            "index_url": self.get_index_url(index_name),
            "authentication": self.get_authentication_config(index_name),
            "connection_settings": self.get_connection_settings(index_name)
        }
    
    def list_all_servers(self) -> list:
        """Get list of all configured server IDs."""
        servers = self.servers_config.get('servers', {})
        return list(servers.keys())
    
    def list_all_indexes(self) -> list:
        """Get list of all configured indexes."""
        index_mappings = self.index_mappings.get('index_mappings', {})
        return list(index_mappings.keys())
    
    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        """
        Get detailed server information.
        
        Args:
            server_id: Unique server identifier
            
        Returns:
            Server information dictionary
        """
        server_config = self.get_server_config(server_id)
        if not server_config:
            return {}
        
        return {
            "server_id": server_id,
            "cluster_url": server_config.get('cluster_url', ''),
            "authentication": server_config.get('authentication', {}),
            "connection_settings": server_config.get('connection_settings', {})
        }
