# Godot Multi-Project Pilot Guide

> 상태: `HISTORICAL_BASE_ADAPTER_REFERENCE_ONLY`
>
> 이 문서는 Base C0 multi-project Pilot의 격리·증거·rollback 설계를 보존하는 역사적 reference다. **현재 Godot persistent authoring 실행 경로가 아니다.** 현재 writer/authoring 권위와 HiGodot·GUT·Hera 역할은 `HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`를 따른다. 이 Pilot은 과거 Base adapter 증거의 감사·회귀·선별 재사용에 한정해 해석한다.

## Status

Base C0 provides a reusable, listener-free validation runner. It is a **static and isolated historical Pilot surface**, not a production transport, a permanent project installation, or a current project-adoption route.

```yaml
multi_project_pilot_runner: STATIC_PASS
real_project_pilots: NOT_RUN
production_adapter_ready: NOT_READY
```

## Immutable cohort

After Base C0 is squash-merged, its merge commit is recorded once as `BASE_C0_SHA`. Every project descriptor and reusable-workflow call pins exactly that SHA. Later movement of Base `main` does not change the cohort. Floating `main` or mutable branch references are forbidden.

## Source checkout and disposable workspace

The caller checkout is the source authority. The runner inventories every Git-tracked byte before and after execution. It creates a disposable workspace outside the source tree, excludes `.git`, `.godot`, prior Pilot evidence, caches, and the checked-out `_base_c0` directory, and never needs to write a product file in the source checkout.

A source inventory mismatch is a hard failure even when the Godot operation itself succeeds.

## Legacy authority boundary

Declared legacy Godot AI editor plugins and `_mcp_game_helper` Autoloads are removed only from the disposable copy. The source `project.godot`, addon, and Autoload remain unchanged. Undeclared project Autoloads are preserved. The Pilot fails closed if a declared legacy authority is missing, if a residual mutation authority remains active, or if a project Autoload is removed to manufacture a PASS.

## Main Scene and scratch Scene

The actual main Scene is opened only for `scene.inspect`. Its physical SHA-256 is measured before and after inspection. All mutation, Editor Undo, save, ledger, and physical-byte verification occur in the runner-owned `res://.godot-live-editor-pilot/scratch.tscn` Scene.

A main Scene byte change is `MAIN_SCENE_READ_ONLY_VIOLATION`.

## Descriptor and behavior checks

The descriptor is closed by JSON Schema. It accepts only three behavior-check kinds:

- `PYTHON_UNITTEST_MODULE`
- `PYTHON_PYTEST_PATH`
- `GODOT_SCRIPT`

There is no command, shell, environment, working-directory, arbitrary argument, arbitrary script, or arbitrary property-path field. Child processes use fixed argv mapping, `shell=False`, explicit timeouts, and bounded output retention.

`NOT_CREATED` descriptors run no Godot process and produce only static `NOT_APPLICABLE` evidence.

## Physical evidence

The runner recomputes hashes from the saved scratch Scene and runtime result bytes. Evidence paths must remain under the disposable workspace and may not use absolute paths, traversal, or symlink escape. The final bounded JSON records exact repository, source commit, `BASE_C0_SHA`, source inventories, runtime result hash, scratch Scene hash, legacy state, and preserved Autoload names.

GitHub Actions artifacts are review inputs with limited retention. Base C1 later revalidates the post-merge artifact whose workflow source SHA equals the squash-merged project commit before promoting bounded evidence into Base.

## Failure and rollback

A Pilot PR changes only its descriptor, adoption document, focused contract test, and caller workflow. Rollback is one revert of those files. A pre-existing project load failure is recorded as blocked evidence; the adoption PR must not patch product code to manufacture PASS.

## Exclusions

Program A does not implement:

- Program B authenticated STDIO MCP transport;
- Program C runtime debugger;
- permanent project installation;
- Windows production operation;
- physical-input validation;
- human editor usability approval.

Program B and Program C require separate brainstorming, design, approval, implementation, and merge gates. This historical statement does not authorize restarting those programs; any current need must first go through the current HiGodot/toolchain policy and Existing Solution First review.
