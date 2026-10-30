# Sharing limits (F4) and the three publish warnings (E6)

- **Editor** access can be granted to individuals only. **Viewer** access to individuals or security groups, and an admin can cap the number of viewers.
- Limits apply to **authenticated** agents only; an unauthenticated agent has no viewer list, which is why "No authentication" is the first warning.
- A tenant-wide share is recorded as `entireTenant` in the inventory (E7) even when no admin approved it, and the pre-publish security scan warns on it.
- The scan's three warnings (no authentication, maker credentials, tenant-wide sharing) are the same three fields `inventory.py` prints first. Read them together.
- An environment-group rule (F2, "agent sharing") can forbid Everyone and restrict Viewer sharing to security groups before a maker ever reaches the dialog.

Do in the portal after `inventory.py`: open the ticket agent → Share → try "Everyone in the tenant" → observe the warning → cancel. Then set the environment-group rule in lab 02 and repeat: the option is gone.
