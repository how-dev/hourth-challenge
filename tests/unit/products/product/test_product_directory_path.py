from unittest.mock import Mock

import freezegun

from apps.products.models import product_directory_path


class TestProductDirectoryPath:
    @freezegun.freeze_time("2022-1-1")
    def test_product_directory_path(self):
        instance = Mock(product_slug="some_slug")
        expected = "media/some_slug_01012022_00:00:00_some_file_name"
        result = product_directory_path(instance=instance, filename="some_file_name")
        assert result == expected
