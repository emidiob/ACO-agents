# ACO Capture — Photographic Image Prompting

ACO Capture converts the user's original idea into a photograph-like image prompt, even when the subject is surreal. It is an **ACO writing and image-direction method**, not a new image generator or proof of model performance.

**When to use:** realistic photographic prompts, documentary or fashion/editorial captures, changing camera viewpoints while keeping a scene consistent, or building a recognizable photographic treatment across a series. Load only the relevant section. One image uses **one coherent capture style**.

## The four ACO Capture layers

**Frame → Moment → Light → Matter**

| Layer | Focus | Compose one sentence about… |
|---|---|---|
| **Frame** | Who/where is the photographer? | photographic medium; plausible lens if useful; viewpoint; framing; crop |
| **Moment** | What is happening, and how does it feel? | mood and atmosphere first, then the user's **subject, action and setting** in the **same** paragraph |
| **Light** | Why is it illuminated this way? | actual light source, direction, quality, spill, contrast and falloff on the subject and background |
| **Matter** | Why does it look physical? | real materials, contact, surface imperfections, motion/environment interaction; grain/noise only when suited to the camera |

**Default output:** one ready-to-paste image prompt in **exactly four short paragraphs** following this order. No section headings inside the prompt. Append a brief labeled Frame / Moment / Light / Matter breakdown **only when useful or requested**.

**Blank working structure:**

```text
Frame: [Photographic style + lens if useful + viewpoint + framing.]
Moment: [Mood and atmosphere; subject + action + setting.]
Light: [Light source + direction + quality + effects on subject and background.]
Matter: [Materials + surface details + physical interactions + appropriate grain/noise.]
```

For **complex prompts**, organize the input internally as **overall look → subjects → décor → finish**, then produce the four layers in the normal order. Do not create a fifth Scene paragraph.

**Rules:** preserve the user's idea and explicit framing, constraints and references. Add only genuinely helpful details; never invent additional subjects, costumes, props, locations or elaborate backstories. Don't add `@image1`, `@image2` or any reference tags unless those files were supplied; preserve their **exact** labels and state what each provides. Camera grain, flash, blur and imperfect framing are optional, not defaults. Avoid “masterpiece”, “8K” and similar empty quality claims. Set 9:16 or another requested aspect ratio in the generator's actual parameter field when supported. Check the current provider's actual input interface; camera words in a prompt are instructions, not a guarantee of reproduction.

## Seven ways to capture an idea

Choose **one** capture mode. Do not stack mutually incompatible camera behaviors. The demonstration scene remains deliberately unchanged to make viewpoint differences observable:

> One person wearing a *real wearable* mascot costume with an oversized head and moustache, a black T-shirt and jeans, sits on a laundromat doorstep at night, holding a carton of fries and looking away from the camera.

This is only a demo subject, not a default scene. Replace the demonstration's subject, action and setting with the user's actual idea.

### 1. Close skate-camera

- **Frame:** Candid 35mm film photograph, 12mm fisheye, very close and shot from knee height; wide framing, curved frame edges, slightly crooked horizon, imperfect skate-photo crop.
- **Moment:** Raw, spontaneous and slightly absurd. The mascot-costumed person sits on the laundromat doorstep with fries, looking away.
- **Light:** Hard direct on-camera flash creates bright foreground detail and hard shadows behind the subject; cool shop fluorescence remains a dim secondary background light.
- **Matter:** Visible fabric and foam of a real costume, denim creases, scuffed shoes, rough asphalt and noticeable film grain.

### 2. Phone snapshot

- **Frame:** Loosely framed vertical phone snapshot from eye level while walking past, slightly tilted with slight photographer motion blur. Set **9:16** in the generator when available.
- **Moment:** Casual, fleeting and unposed. The same mascot-costumed person sits on the laundromat doorstep, holding fries and looking away.
- **Light:** Doorway fluorescents spill on one side of the costume. Weak street illumination leaves uneven light and noisy shadows.
- **Matter:** Real costume seams, foam surface, cotton folds, denim creases and phone-camera noise in darker regions.

### 3. Intimate documentary

- **Frame:** Close handheld photograph on 35mm film with a 35mm lens, at the seated subject's eye level, waist-up, slightly uneven crop.
- **Moment:** Quiet, observational and unguarded. The same mascot-costumed person sits on the doorstep, holding fries and turning their head away.
- **Light:** Uneven fluorescence from the laundromat grazes one side, soft shadow on the other; dim but readable background.
- **Matter:** Costume seams and foam, fabric folds at elbows, grease marks on the carton and fine film grain.

### 4. Motion-blurred photo dump

- **Frame:** Badly shaken handheld phone snapshot with pronounced *directionally consistent* diagonal camera-shake blur across subject **and background**, doubled edges and still-recognizable smeared forms.
- **Moment:** Chaotic, accidental and slightly absurd. The same costumed person is caught holding fries on the doorstep.
- **Light:** Available shop fluorescents and weak streetlights; bright regions streak in the same direction as the camera shake.
- **Matter:** Fabric, foam and denim dissolve into soft texture blocks, shadow noise, pavement smeared by camera motion.

### 5. Low curbside

- **Frame:** 24mm wide-angle photo from curb level, full-body; shoes large near the camera, costume head further away, pavement dominant in the foreground.
- **Moment:** Mundane, unposed and quietly comic. The same seated person holds fries and looks away outside the laundromat.
- **Light:** Cool storefront fluorescence hits the curb and figure; weak streetlight catches foreground pavement, deeper shadow under the legs.
- **Matter:** Actual fabric and foam, denim bunching at knees, scuffed shoes and coarse pavement close to the lens.

### 6. Compact-camera flash

- **Frame:** Spontaneous night photograph on a cheap *digital point-and-shoot* camera, much of the image in focus, quick imperfect crop.
- **Moment:** Candid, mundane and slightly absurd. The same mascot-costumed person sits on the doorstep with fries, looking away.
- **Light:** Hard built-in frontal flash makes a sharp cast shadow and some clipped highlights, with the shop faint in a darker background.
- **Matter:** Costume foam, creased denim, slightly crunchy digital detail, mild compression artifacts and noisy shadows.

**Note:** A disposable **film** camera and a cheap **digital** point-and-shoot aren't the same capture medium. If the user asks for disposable film, choose actual disposable film behavior and remove digital compression artifacts.

### 7. Concealed observation

- **Frame:** Distant telephoto photo from inside a parked car, compressed perspective, slightly soft focus; blurred window edge and dashboard partly obscure foreground.
- **Moment:** Quiet, distant and unposed. The same mascot-costumed person sits across the street, looking away, unaware of the camera.
- **Light:** Laundromat fluorescence illuminates the subject across the road; dark car interior and uneven street light around the pavement.
- **Matter:** Real costume foam and fabric, creased denim, rough pavement, subtle camera grain and faint window-glass reflections.

**Compare actual results:** keeping the example scene fixed, test whether viewpoint, lens perspective, crop, light and blur really changed. Never claim success without seeing the produced image.

## Reusable preset: ACO Capture / Night Fisheye Flash

Use this for a consistent late-night **DIY street editorial / skate-documentary** signature. Replace the subject, pose/action, clothes, props and setting, but preserve these **five visual invariants** across the series:

1. **12mm fisheye** look with a *very close* camera at a *low, near-ground* viewpoint.
2. Strong barrel distortion and exaggerated near-field scale, while still showing the surrounding environment.
3. **Hard direct on-camera flash** dominant over ambient light; flash-frozen foreground and fast falloff into nighttime darkness.
4. Slightly crooked, imperfect street-photo framing, crisp specular highlights, strong local contrast and dense but readable blacks.
5. Restrained visible **35mm-style film grain**, mild highlight bloom only on reflective surfaces, no beauty-fill softness or HDR-like shadow recovery.

**Prompt-ready four-paragraph version — substitute the Moment paragraph:**

Extremely close low-angle environmental photograph at night, near-ground 12mm fisheye lens, strong barrel distortion and exaggerated foreground scale. The subject fills much of the frame while retaining a broad slice of the environment, with a crooked horizon and spontaneous imperfect crop.

Raw, direct and slightly awkward, like a late-night documentary skate photograph taken from right inside the action. [Describe the user's actual subject, action and setting.]

Hard direct on-camera flash dominates the exposure, producing bright crisp foreground highlights, sharp local contrast and rapid falloff into much darker surroundings. Reflective objects catch sharp white speculars; ambient practical lights remain dim and secondary, corners in deep shadow.

Physically coherent surface wear, fabric, folds, scuffs and material contact with the environment. Flash-frozen foreground with rough analog-style tonal response, restrained 35mm film grain, dense but readable blacks and subtle bloom only where surfaces are genuinely reflective. No studio beauty fill or HDR shadow lifting.

**Short camera-style version:**

`Very close 12mm fisheye at night, low near-ground viewpoint, exaggerated foreground perspective, curved edges and crooked skate-photo framing, hard direct on-camera flash, crisp foreground speculars and fast falloff to deep ambient shadows, restrained 35mm film grain, raw DIY street editorial.`

**Keep this coherent:** don't simultaneously request a concealed telephoto shot, eye-level passing phone snapshot, natural-light-only exposure or full-frame camera-shake blur. If a hybrid is expressly requested, reconcile the physical camera and lighting behavior first.

## Acceptance review

1. **Fidelity:** subject, action and setting preserved; no extra subjects or unrequested props.
2. **Frame:** one internally coherent camera, lens behavior, viewpoint and crop.
3. **Light:** physically plausible light directions, cast shadows, falloff and specular highlights.
4. **Matter:** material detail arises from actual surfaces, wear, movement and environment.
5. **References:** exact supplied reference labels and roles preserved; no invented image references.
6. **Variation:** when comparing captures, *photographic treatment* changes but the underlying scene does not.
7. **QC:** inspect actual renders when available; don't confuse a good prompt with proven image-generation performance.

The method may be applied directly as a **playbook** through ACO Concierge, Art Director or Production Office. Existing Nano Banana and Seedream **technical skill candidates** remain non-selectable until separate live evaluation and explicit promotion. The playbook itself does not grant tool access, install a provider, or prove image quality.

**Source and provenance:** adapted into ACO terminology from the user-provided realistic-photo template, Seven Ways to Capture an Idea and Night Fisheye Flash direction shared on 2026-10-19. No supplied image references, proprietary files, third-party models or credentials are bundled.
