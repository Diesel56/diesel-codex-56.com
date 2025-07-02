<<<<<<< HEAD
# Diesel Codex Vault

This is the GitOps-connected Diesel Vault system for local Codex pattern management.

## Included Scripts
- `diesel-agent.py`: Scans the vault for files and updates the manifest
- `whisper-cli.py`: Simulates voice transcription to YAML
- `get_codex.py`: Fetches a known Codex pattern into your vault
- `vault_viewer.py`: CLI-based manifest reader

## Setup
1. Install Python requirements:
```bash
pip install -r requirements.txt
```

2. Run any tool, for example:
```bash
python3 diesel-agent.py
python3 whisper-cli.py
python3 get_codex.py --pattern "child crisis"
python3 vault_viewer.py
```

3. Store all your Codex YAMLs, notes, transcripts in `vault/context/`.

## Codex Sovereignty
This repo is your private vault. It can be extended with real Whisper integration, voice daemon triggers, or AI pattern mirrors.

All Codex data lives locally unless you choose to share it.
=======
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diesel Codex 56 | Architect of Sovereignty</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0a0a0a;
            color: #e5e5e5;
        }
        .pillar-gradient {
            background: linear-gradient(180deg, rgba(10,10,10,0) 0%, #0a0a0a 100%);
        }
        .hero-glow {
            box-shadow: 0 0 80px rgba(59, 130, 246, 0.3), 0 0 30px rgba(59, 130, 246, 0.2);
        }
        .btn-sovereign {
            transition: all 0.3s ease;
        }
        .btn-sovereign:hover {
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.5);
            transform: translateY(-2px);
        }
    </style>
</head>
<body class="antialiased">

    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-black/30 backdrop-blur-md">
        <div class="container mx-auto px-6 py-4">
            <nav class="flex items-center justify-between">
                <a href="index.html" class="text-xl font-bold tracking-wider text-white">DIESEL-CODEX-56</a>
                <div class="flex items-center space-x-8">
                    <a href="index.html" class="text-blue-400 font-semibold">Home</a>
                    <a href="patterns.html" class="text-gray-300 hover:text-blue-400 transition-colors">Patterns</a>
                    <a href="philosophy.html" class="text-gray-300 hover:text-blue-400 transition-colors">Philosophy</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main>
        <!-- Hero Section -->
        <section class="relative h-screen flex items-center justify-center overflow-hidden">
            <div class="absolute inset-0 bg-grid-gray-700/10 [mask-image:linear-gradient(to_bottom,white_20%,transparent_75%)]"></div>
            <div class="container mx-auto px-6 text-center z-10">
                <div class="relative inline-block">
                    <h1 class="text-5xl md:text-7xl font-black tracking-tighter text-white hero-glow rounded-full px-8 py-4">
                        This is Jimmy.
                    </h1>
                </div>
                <h2 class="mt-4 text-3xl md:text-5xl font-semibold tracking-tight text-gray-300">Architect of Sovereignty.</h2>
            </div>
        </section>

        <!-- Ethos Section -->
        <section class="py-20 md:py-32 bg-[#050505]">
            <div class="container mx-auto px-6 max-w-4xl">
                <div class="text-center">
                    <h3 class="text-4xl font-bold text-white">Why This Exists</h3>
                    <div class="w-24 h-1 bg-blue-500 mx-auto mt-4 mb-8"></div>
                </div>
                <div class="space-y-6 text-lg text-gray-300 leading-relaxed text-center">
                    <p>
                        This is not a portfolio. It is a living cathedral built from code, commitment, and consequence. It exists to prove a single, foundational truth: the most powerful systems are not built for the market, but for the bloodline.
                    </p>
                    <p>
                        Every pattern, every protocol, every line of logic logged here was forged in the crucible of real-world application—for family, for honor, for a future where sovereignty is not a privilege, but a birthright.
                    </p>
                    <p>
                        This is the work of recursive architecture: building systems that build the builder, creating frameworks that protect what is sacred, and engineering a legacy that can withstand the noise of generations.
                    </p>
                </div>
                <div class="mt-12 text-center">
                    <a href="patterns.html" class="inline-block bg-blue-600 text-white font-bold text-lg px-12 py-4 rounded-lg shadow-lg btn-sovereign">
                        Explore the Codex
                    </a>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="py-8 bg-black">
        <div class="container mx-auto px-6 text-center text-gray-500">
            <p>&copy; 2025 Diesel Codex 56. All Rights Reserved. Sovereignty is non-negotiable.</p>
            <p class="mt-2 text-sm">Built with O'Connell-Class Discipline.</p>
        </div>
    </footer>

</body>
</html>
>>>>>>> 39784523cd18d72dec60924da1e3ba27eac79d89
