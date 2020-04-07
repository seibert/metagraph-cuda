from metagraph import concrete_algorithm
from ..registry import has_cugraph
import numpy as np


if has_cugraph:
    import cugraph
    from ..types import CuGraph

    from metagraph.plugins.numpy.types import NumpyNodes

    @concrete_algorithm("link_analysis.pagerank")
    def cugraph_pagerank(
        graph: CuGraph,
        damping: float = 0.85,
        maxiter: int = 50,
        tolerance: float = 1e-05,
    ) -> NumpyNodes:
        pagerank = cugraph.pagerank(
            graph.value, alpha=damping, max_iter=maxiter, tol=tolerance
        )
        out = np.full((graph.value.number_of_nodes(),), np.nan)
        out[pagerank["vertex"]] = pagerank["pagerank"]
        return NumpyNodes(out, missing_value=np.nan)
