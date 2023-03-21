import enum

Condition = enum.Enum(
    value='Condition',
    names=('DEFAULT', 'FREE', 'BUSY', 'STOPPED'),
)