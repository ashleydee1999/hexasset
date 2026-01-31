
```md
# hexasset

Find Xcode colour assets (`.colorset`) by hex value by scanning `.xcassets` in a repo.

## Clone

```bash
git clone git@github.com:ashleydee1999/hexasset.git
cd hexasset

```

## Install (pipx, recommended)

```bash
brew install pipx
pipx ensurepath
# restart your terminal
pipx install "git+ssh://git@github.com:ashleydee1999/hexasset.git"

```

Verify:

```bash
hexasset --help

```

## Usage

Run inside an iOS repo:

```bash
hexasset FF0000

```

Other accepted formats:

```bash
hexasset 0xFF0000
hexasset "#FF0000"

```

Scan a specific path:

```bash
hexasset FF0000 /path/to/repo

```

## Output + exit codes

-   Match found: prints `ColorName alpha = X`, exits `0`
    
-   No match: prints `NO_MATCH`, exits `1`
    
-   Invalid input: prints an error, exits `2`
