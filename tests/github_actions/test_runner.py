import unittest
from pathlib import Path

from checkov.github_actions.runner import Runner
from checkov.runner_filter import RunnerFilter


class TestRunnerValid(unittest.TestCase):
    def test_runner(self):
        # given
        test_dir = Path(__file__).parent / "resources"
        checks = ["CKV_GHA_1", "CKV_GHA_2"]

        # when
        report = Runner().run(
            root_folder=str(test_dir), runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        self.assertEqual(len(report.failed_checks), 9)
        self.assertEqual(len(report.parsing_errors), 0)
        self.assertEqual(len(report.passed_checks), 131)
        self.assertEqual(len(report.skipped_checks), 0)

    def test_runner_on_suspectcurl(self):
        # given
        file_path = Path(__file__).parent / "resources/.github/workflows/suspectcurl.yaml"
        file_dir = [str(file_path)]
        checks = ["CKV_GHA_1", "CKV_GHA_3"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.failed_checks[0].job[0] == 'prep'
        assert report.failed_checks[0].triggers[0] == {'push', 'workflow_dispatch'}
        assert report.failed_checks[0].workflow_name == 'CI'

        assert report.failed_checks[1].job[0] == 'build'
        assert report.failed_checks[1].triggers[0] == {'push', 'workflow_dispatch'}
        assert report.failed_checks[1].workflow_name == 'CI'

    def test_runner_on_shell_injection(self):
        # given
        file_path = Path(__file__).parent / "resources/.github/workflows/shell_injection.yaml"
        file_dir = [str(file_path)]
        checks = ["CKV_GHA_1", "CKV_GHA_3"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.passed_checks[0].job[0] == 'unsecure-job'
        assert report.passed_checks[0].triggers[0] == {'issues'}
        assert report.passed_checks[0].workflow_name == 'unsec33ure-worfklow'

        assert report.passed_checks[1].job[0] == 'secure-job'
        assert report.passed_checks[1].triggers[0] == {'issues'}
        assert report.passed_checks[1].workflow_name == 'unsec33ure-worfklow'

        assert report.passed_checks[2].job[0] == 'unsecure-steps'
        assert report.passed_checks[2].triggers[0] == {'issues'}
        assert report.passed_checks[2].workflow_name == 'unsec33ure-worfklow'

    def test_runner_on_netcatreverseshell(self):
        # given
        file_path = Path(__file__).parent / "resources/.github/workflows/netcatreverseshell.yaml"
        file_dir = [str(file_path)]
        checks = ["CKV_GHA_1", "CKV_GHA_3"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.passed_checks[0].job[0] == 'prep'
        assert report.passed_checks[0].triggers[0] == {'workflow_dispatch', 'push'}
        assert report.passed_checks[0].workflow_name == 'REVERSESHELL'

        assert report.passed_checks[1].job[0] == 'build'
        assert report.passed_checks[1].triggers[0] == {'workflow_dispatch', 'push'}
        assert report.passed_checks[1].workflow_name == 'REVERSESHELL'

    def test_runner_on_unsecure_command(self):
        # given
        file_path = Path(__file__).parent / "resources/.github/workflows/unsecure_command.yaml"
        file_dir = [str(file_path)]

        checks = ["CKV_GHA_1", "CKV_GHA_3"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.failed_checks[0].job[0] == 'unsecure-job'
        assert report.failed_checks[0].triggers[0] == {'pull_request'}
        assert report.failed_checks[0].workflow_name == 'unsecure-worfklow'

        assert report.passed_checks[2].job[0] == 'secure-job'
        assert report.passed_checks[2].triggers[0] == {'pull_request'}
        assert report.passed_checks[2].workflow_name == 'unsecure-worfklow'

    def test_runner_on_non_empty_workflow_dispatch(self):
        # given
        file_path = Path(__file__).parent / "resources/.github/workflows/workflow_dispatch.yaml"
        file_dir = [str(file_path)]

        checks = ["CKV_GHA_7"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.failed_checks[0].job[0] == None
        assert report.failed_checks[0].triggers[0] == {'workflow_dispatch'}
        assert report.failed_checks[0].workflow_name == None

    def test_runner_on_list_typed_workflow_dispatch(self):
        # given
        file_path = Path(__file__).parent / "resources/.github/workflows/list_workflow_dispatch.yaml"
        file_dir = [str(file_path)]

        checks = ["CKV_GHA_7"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert len(report.failed_checks) == 0

    def test_runner_on_supply_chain(self):
        # given
        file_path = Path(__file__).parent / "resources/.github/workflows/supply_chain.yaml"
        file_dir = [str(file_path)]
        checks = ["CKV_GHA_1", "CKV_GHA_3"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.failed_checks[0].job[0] == "bridgecrew"
        assert report.failed_checks[0].triggers[0] == {"workflow_dispatch", "schedule"}
        assert report.failed_checks[0].workflow_name == 'Supply Chain'

        assert report.passed_checks[1].job[0] == "bridgecrew2"
        assert report.passed_checks[1].triggers[0] == {"workflow_dispatch", "schedule"}
        assert report.passed_checks[1].workflow_name == 'Supply Chain'

    def test_runner_on_build(self):
        # given
        file_path = Path(__file__).parent.parent.parent / ".github/workflows/build.yml"
        file_dir = [str(file_path)]
        checks = ["CKV_GHA_1", "CKV_GHA_3"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.failed_checks[0].job[0] == 'update-bridgecrew-projects'
        assert report.failed_checks[0].triggers[0] == {'workflow_dispatch', 'push'}
        assert report.failed_checks[0].workflow_name == 'build'

        assert report.passed_checks[6].job[0] == "publish-checkov-admissioncontroller-dockerhub"
        assert report.passed_checks[6].triggers[0] == {'workflow_dispatch', 'push'}
        assert report.passed_checks[6].workflow_name == 'build'

    def test_runner_on_codeql_analysis(self):
        # given
        file_path = Path(__file__).parent.parent.parent / ".github/workflows/codeql-analysis.yml"
        file_dir = [str(file_path)]
        checks = ["CKV_GHA_1", "CKV_GHA_3"]

        # when
        report = Runner().run(
            files=file_dir, runner_filter=RunnerFilter(framework=["github_actions"], checks=checks)
        )

        # then
        assert report.passed_checks[0].job[0] == "analyze"
        assert report.passed_checks[0].triggers[0] == {'push', 'schedule', 'pull_request', 'workflow_dispatch'}
        assert report.passed_checks[0].workflow_name == 'CodeQL'


if __name__ == "__main__":
    unittest.main()
