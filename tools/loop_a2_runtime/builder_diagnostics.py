from __future__ import annotations


class BuilderStageError(RuntimeError):
    """Stable private exception base used only to classify unexpected Builder stages."""


class BuilderWorkspacePreparationError(BuilderStageError):
    pass


class BuilderWorkerInvocationError(BuilderStageError):
    pass


class BuilderDiffCollectionError(BuilderStageError):
    pass


class BuilderResultBindingError(BuilderStageError):
    pass
