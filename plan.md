# Cookbook Implementation Plan

## Product summary

Cookbook is a recipe management platform with:

- FastAPI backend (auth, users, recipes, ingredients)
- React Router web app (partially implemented)
- Shared OpenAPI types package
- Mobile app workspace (currently minimal)

This plan prioritizes completing core web product flows first, then hardening backend behavior, then adding expansion features.

## Milestones

1. Stabilize the baseline.
2. Ship core web workflow.
3. Make recipe experience fully usable.
4. Harden backend rules and permissions.
5. Expand into higher-value product features.
6. Keep delivery sustainable with tests and type safety.

## Task backlog (prioritized)

### M1 - Stabilize baseline (P0)

- Audit route coverage and mark each route implemented, partial, or stubbed.
- Verify backend endpoint coverage for auth/users/recipes/ingredients.
- Regenerate shared OpenAPI types and confirm no drift.
- Define route-level Definition of Done: loading, error, empty, success, auth behavior.

### M2 - Core web workflow (P0)

- Implement register route with validation and backend error handling.
- Implement profile route using current-user API.
- Implement ingredients route with list/create/update/delete UI.
- Implement recipe create route (ingredients, steps, visibility).
- Implement recipe edit route with prefilled data and update flow.
- Fix recipes list loading blink by preserving existing data during refetch.

### M2 UX polish (P1)

- Add consistent inline error banners across auth and CRUD routes.
- Add empty-state UX for recipes and ingredients.
- Improve mutation UX with optimistic updates or immediate refetch.
- Show recipe hints/suggestions under the ingredients list while composing or editing a recipe.

### M3 - Recipe usability and discovery (P1)

- Expand recipe detail view to show full steps, ingredients, units, tags, visibility, and owner actions.
- Add search by recipe name/description.
- Add filter by recipe tags.
- Add filters for diet type, meal type, and visibility.
- Add search for recipes by available ingredients (pantry-style lookup).
- Add sorting (recent, name, prep time).
- Add pagination or incremental loading.

### M4 - Backend hardening (P1)

- Enforce disabled-user checks in auth dependency flow.
- Review and tighten role/permission boundaries.
- Add password change/reset flow design and endpoint implementation.
- Decide tags strategy: implicit creation vs dedicated CRUD endpoints.
- Add rate limiting and improve validation error consistency.

### M5 - Product expansion (P2)

- Add recipe photos/media upload and storage strategy.
- Add favorites/saved recipes model and endpoints.
- Add ratings/reviews model and moderation rules.
- Add sharing/collaboration flows aligned with existing visibility.

### M6 - Quality and delivery (Continuous, P0)

- Add web tests for hooks and route loading/error/mutation states.
- Add end-to-end test coverage for critical user journeys (auth, recipe discovery, create/edit recipe, ingredient management).
- Keep backend tests updated for every new endpoint/permission rule.
- Keep shared type generation in API-change workflow.
- Deliver features in vertical slices with one clear user-visible outcome.

## Suggested sprint sequence

1. Sprint 1: M1 + recipes loading blink fix.
2. Sprint 2: register/profile + ingredients completion.
3. Sprint 3: recipe create/edit/detail completion.
4. Sprint 4: search/filter/sort/pagination + mutation UX polish.
5. Sprint 5: backend hardening.
6. Sprint 6+: expansion features.

## Suggested first tickets

1. Fix recipes stale-while-refresh behavior in web hooks and list route.
2. Complete register route with validation and user feedback.
3. Complete ingredients route using existing components.
4. Complete recipe create and edit flows.
5. Expand recipe detail from card-only to full detail page.
6. Set up e2e test suite and add smoke coverage for login, recipes list, recipe create, and ingredient CRUD.

## Feature breakdown: requested additions

### 1) Filter recipes by tags

- Backend
  - Add tags query parameter to recipes listing endpoint (single or multiple tags).
  - Update recipe service query logic to filter by related tags.
  - Keep behavior composable with existing filters (diet, meal type, visibility).
- Web
  - Add tags filter control to recipes list UI (multi-select or token input).
  - Sync selected tags to URL search params for shareable filtered views.
  - Update recipe fetching hook to pass selected tags to API.
- Testing
  - Add backend tests for tag-only and combined-filter queries.
  - Add web tests for filter state, URL sync, and filtered list rendering.

### 2) Show recipe hints under ingredients list

- Product behavior
  - Display context hints directly under ingredients list while creating/editing recipes.
  - Hints can include substitutions, missing pairings, unit guidance, or common combinations.
- Backend (if dynamic hints)
  - Add optional endpoint/service for hint generation from current ingredient set.
  - Return deterministic hint payload shape for stable UI rendering.
- Web
  - Create a hints panel component below ingredients list.
  - Trigger hints refresh when ingredient rows change (debounced).
  - Provide loading and empty states that do not disrupt form editing.
- Testing
  - Add component tests for hint visibility, empty hints, and update behavior.

### 3) Search recipes by available ingredients

- Backend
  - Add include_ingredients query support in recipes listing/search endpoint.
  - Support exact and partial match modes (all ingredients vs any ingredient).
  - Include optional scoring (more matching ingredients ranks higher).
- Web
  - Add "I have these ingredients" input in recipes discovery UI.
  - Provide ingredient token selection from known ingredients.
  - Render match confidence details (for example: "5/7 ingredients matched").
- Testing
  - Add backend tests for all/any matching modes and ranking.
  - Add web tests for ingredient token input and result ranking display.

## Suggested delivery order for new additions

1. Tag filter first (lowest risk, fastest value).
2. Ingredient-based search second (high user value, moderate backend work).
3. Recipe hints third (depends on hint rules/design decisions).
