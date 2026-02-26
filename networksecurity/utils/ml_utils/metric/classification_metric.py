import os, sys
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception

def get_classification_metric(y_true, y_pred) -> ClassificationMetricArtifact:    
    try:
        model_metrics = ClassificationMetricArtifact(f1_score=f1_score(y_true, y_pred),
                                                    precision_score=precision_score(y_true, y_pred),
                                                    recall_score=recall_score(y_true, y_pred),
                                                    accuracy_score=accuracy_score(y_true, y_pred))
        return model_metrics
    except Exception as e:
        raise custom_exception(e, sys)