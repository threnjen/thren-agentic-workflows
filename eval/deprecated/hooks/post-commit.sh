#!/usr/bin/env sh

json_escape() {
    input=$1
    output=
    tab=$(printf '\t')
    carriage_return=$(printf '\r')

    while [ -n "$input" ]; do
        char=$(printf '%.1s' "$input")
        input=${input#?}

        case "$char" in
            '\\')
                output=$output'\\\\'
                ;;
            '"')
                output=$output'\\"'
                ;;
            "$tab")
                output=$output'\\t'
                ;;
            "$carriage_return")
                output=$output'\\r'
                ;;
            *)
                output=$output$char
                ;;
        esac
    done

    printf '%s' "$output"
}

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || printf 'HEAD')

case "$branch" in
    phase/*)
        ;;
    *)
        exit 0
        ;;
esac

repo_root=$(git rev-parse --show-toplevel 2>/dev/null || printf '')

if [ -z "$repo_root" ]; then
    exit 0
fi

slug=phase
branch_tail=${branch#phase/}

while :; do
    case "$branch_tail" in
        */*)
            slug="$slug-${branch_tail%%/*}"
            branch_tail=${branch_tail#*/}
            ;;
        *)
            slug="$slug-$branch_tail"
            break
            ;;
    esac
done

ledger_dir="$repo_root/eval/runs/$slug"
ledger_file="$ledger_dir/ledger-commits.jsonl"

mkdir -p "$ledger_dir" 2>/dev/null || exit 0

sha=$(git rev-parse HEAD 2>/dev/null || printf '')
message=$(git log -1 --pretty=%s 2>/dev/null || printf '')
timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || printf '')
changed_files=$(git -c core.quotePath=true diff-tree --no-commit-id --root -r --name-only HEAD 2>/dev/null || printf '')

files_json=
separator=

while IFS= read -r path; do
    if [ -z "$path" ]; then
        continue
    fi

    case "$path" in
        \"*\")
            escaped_path=${path#\"}
            escaped_path=${escaped_path%\"}
            ;;
        *)
            escaped_path=$(json_escape "$path")
            ;;
    esac

    files_json=$files_json$separator\"$escaped_path\"
    separator=,
done <<EOF
$changed_files
EOF

escaped_branch=$(json_escape "$branch")
escaped_message=$(json_escape "$message")

printf '{"sha":"%s","branch":"%s","message":"%s","timestamp":"%s","files":[%s]}\n' \
    "$sha" \
    "$escaped_branch" \
    "$escaped_message" \
    "$timestamp" \
    "$files_json" >> "$ledger_file" 2>/dev/null || true

exit 0