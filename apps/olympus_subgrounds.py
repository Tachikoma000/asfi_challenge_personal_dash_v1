from datetime import datetime

import dash
from dash import html

from subgrounds.dash_wrappers import Graph
from subgrounds.plotly_wrappers import Figure, Scatter, Indicator
from subgrounds.schema import TypeRef
from subgrounds.subgraph import SyntheticField
from subgrounds.subgrounds import Subgrounds


sg = Subgrounds()
olympusDAO = sg.load_subgraph('https://api.thegraph.com/subgraphs/name/drondin/olympus-graph')

# Define useful synthetic fields
olympusDAO.ProtocolMetric.datetime = SyntheticField(
  lambda timestamp: str(datetime.fromtimestamp(timestamp)),
  TypeRef.Named('String'),
  olympusDAO.ProtocolMetric.timestamp,
)

olympusDAO.ProtocolMetric.staked_supply_percent = 100 * olympusDAO.ProtocolMetric.sOhmCirculatingSupply / olympusDAO.ProtocolMetric.totalSupply
olympusDAO.ProtocolMetric.unstaked_supply_percent = 100 - olympusDAO.ProtocolMetric.staked_supply_percent

olympusDAO.ProtocolMetric.rfv_per_ohm = olympusDAO.ProtocolMetric.treasuryRiskFreeValue / olympusDAO.ProtocolMetric.totalSupply
olympusDAO.ProtocolMetric.price_rfv_ratio = 100 * olympusDAO.ProtocolMetric.ohmPrice / (olympusDAO.ProtocolMetric.rfv_per_ohm + 1)

olympusDAO.ProtocolMetric.tmv_per_ohm = olympusDAO.ProtocolMetric.treasuryMarketValue / olympusDAO.ProtocolMetric.totalSupply
olympusDAO.ProtocolMetric.price_tmv_ratio = 100 * olympusDAO.ProtocolMetric.ohmPrice / (olympusDAO.ProtocolMetric.tmv_per_ohm + 1)

protocol_metrics_1year = olympusDAO.Query.protocolMetrics(
  orderBy=olympusDAO.ProtocolMetric.timestamp,
  orderDirection='desc',
  first=365
)

last_metric = olympusDAO.Query.protocolMetrics(
  orderBy=olympusDAO.ProtocolMetric.timestamp,
  orderDirection='desc',
  first=1
)