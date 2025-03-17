import ast
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class FunctionExtractor(ast.NodeVisitor):
    def __init__(self, target_name: str):
        """
        target_name: 'function_name'
        """
        self.target_name = target_name
        self.found_node = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == self.target_name:
            self.found_node = node
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if node.name == self.target_name:
            self.found_node = node
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == self.target_name:
                self.found_node = item
        self.generic_visit(node)


def extract_function_code(repo_path: str, function_full_name: str) -> Optional[str]:
    parts = function_full_name.split('.')
    logger.info(parts)
    if len(parts) < 2:
        logger.error("❗️ Invalid function name format. Use module.function or module.Class.method")
        return None
    module_parts = parts[:-1]
    function_name = parts[-1]
    module_path = os.path.join(repo_path, *module_parts) + '.py'

    logger.info(f"🔎 Looking for module file: {module_path}")
    if not os.path.exists(module_path):
        logger.error("❗️ Module file not found!")
        return None

    with open(module_path, 'r', encoding='utf-8') as f:
        source = f.read()
    tree = ast.parse(source)
    extractor = FunctionExtractor(function_name)
    extractor.visit(tree)

    if extractor.found_node:
        func_code = ast.get_source_segment(source, extractor.found_node)
        logger.info("✅ Function found!")
        logger.info(func_code)
        return func_code
